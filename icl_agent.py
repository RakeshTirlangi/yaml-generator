import yaml
from pypdf import PdfReader
import google.generativeai as genai
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re
from dotenv import load_dotenv

load_dotenv()

class ICLAgent:
    def __init__(self, doc_path: str, api_key: str, output_dir: str = "configs"):
        """Initialize the ICL Agent with necessary configurations."""
        self.doc_path = doc_path
        self.output_dir = output_dir
        self.knowledge = {}
        
        os.makedirs(output_dir, exist_ok=True)  

        
        genai.configure(api_key=api_key)
        generation_config = {
            "temperature": 0.1,  
            "top_p": 0.8,
            "top_k": 40,
        }
        self.model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
        
       
        self.log("Initializing and loading documentation...")
        self._load_knowledge()

    def log(self, message: str, type: str = "info") -> None:
        """Unified logging with emoji indicators."""
        indicators = {
            "info": "ℹ️",
            "think": "🤔",
            "action": "🎯",
            "error": "❌",
            "success": "✅"
        }
        prefix = indicators.get(type, "ℹ️")
        print(f"{prefix} {message}")

    def _clean_response(self, text: str) -> str:
        """Cleans model response to ensure valid YAML formatting."""
        if not text:
            return ""
        
       
        text = re.sub(r'```[yamlYAML]*\n', '', text)  # Remove opening ```
        text = text.replace('```', '')  # Remove closing ```
        
      
        text = re.sub(r'#.*$', '', text, flags=re.MULTILINE)
        
       
        lines = text.strip().splitlines()
        cleaned_lines = [line.replace('\t', '  ') for line in lines if line.strip()]
        
        return '\n'.join(cleaned_lines)

    def _parse_yaml_safely(self, content: str) -> Dict:
        """Safely parses YAML content, handling multiple documents properly."""
        try:
            docs = list(yaml.safe_load_all(content))  
            if not docs:
                raise ValueError("Empty YAML content")
            return docs[0] if len(docs) == 1 else {"documents": docs}  
        except yaml.YAMLError as e:
            self.log(f"YAML parsing failed: {str(e)}", "error")
            return {"error": "Failed to parse YAML", "timestamp": str(datetime.now())}

    def _save_yaml(self, data: Dict, name: str = None) -> str:
        """Saves the YAML content to a file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.yaml" if name else f"config_{timestamp}.yaml"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            self.log(f"Configuration saved to {filepath}", "success")
            return filepath
        except Exception as e:
            self.log(f"Error saving YAML: {str(e)}", "error")
            raise

    def _load_knowledge(self) -> None:
        """Extracts key knowledge from the ICL PDF documentation."""
        try:
            self.log("Reading documentation...", "think")

            if not os.path.exists(self.doc_path):
                raise FileNotFoundError(f"Documentation file not found: {self.doc_path}")

            reader = PdfReader(self.doc_path)
            content = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

            self.log("Extracting key information...", "think")

            prompt = """
            Extract key information from the documentation and format it as YAML with the following structure:
            schema:
              components: []
              parameters: []
            rules:
              validation: []
              security: []
            practices:
              deployment: []
              configuration: []
            patterns:
              common: []
              recommended: []

            Output **only valid YAML**, without markdown formatting or extra text.
            """
            
            response = self.model.generate_content([prompt, content])
            knowledge = self._parse_yaml_safely(self._clean_response(response.text))

            if not isinstance(knowledge, dict) or not knowledge:
                raise ValueError("Invalid knowledge structure")
            
            self.knowledge = knowledge
            self.log("Documentation processed successfully", "success")
        except Exception as e:
            self.log(f"Error loading documentation: {str(e)}", "error")
            self.knowledge = {
                "schema": {"components": [], "parameters": []},
                "rules": {"validation": [], "security": []},
                "practices": {"deployment": [], "configuration": []},
                "patterns": {"common": [], "recommended": []}
            }

    def process_request(self, user_input: str) -> Tuple[Dict, str]:
        """Generates an ICL YAML configuration based on user input."""
        try:
            self.log(f"Processing request: {user_input}", "think")

            prompt = f"""
            Generate a YAML configuration based on this request: {user_input}

            Knowledge base:
            {yaml.dump(self.knowledge, default_flow_style=False)}

            Requirements:
            - Output **only valid YAML**, without markdown or extra text.
            - Ensure all necessary components are included.
            - Follow security and best practices.
            - Use proper indentation.

            Response must be **pure YAML** with no extra formatting.
            """
            
            response = self.model.generate_content(prompt)
            config = self._parse_yaml_safely(self._clean_response(response.text))
            filepath = self._save_yaml(config, "icl_config")

            return config, filepath
        except Exception as e:
            self.log(f"Error processing request: {str(e)}", "error")
            raise

    def update_configuration(self, current_config: Dict, update_request: str) -> Tuple[Dict, str]:
        """Updates an existing configuration based on user request."""
        try:
            self.log(f"Processing update: {update_request}", "think")

            prompt = f"""
            Update this configuration:
            {yaml.dump(current_config, default_flow_style=False)}

            With these changes: {update_request}

            Knowledge base:
            {yaml.dump(self.knowledge, default_flow_style=False)}

            Requirements:
            - Maintain existing valid settings.
            - Update only the necessary parts.
            - Ensure structure and format remain valid.
            - Ensure correct indentation.

            Response must be **pure YAML** with no extra text.
            """
            
            response = self.model.generate_content(prompt)
            updated_config = self._parse_yaml_safely(self._clean_response(response.text))
            filepath = self._save_yaml(updated_config, "icl_config_updated")

            return updated_config, filepath
        except Exception as e:
            self.log(f"Error updating configuration: {str(e)}", "error")
            raise

def icl_agent():
    try:
        agent = ICLAgent(doc_path="icl.pdf", api_key=os.getenv("GEMINI_API_KEY"))

        print("\n📝 Generating initial configuration...")
        config, filepath = agent.process_request("Deploy a Node.js app with auto-scaling and 2GB RAM in a secured region")
        print(f"\nConfiguration saved to: {filepath}")

        print("\n📝 Updating configuration...")
        updated_config, updated_filepath = agent.update_configuration(config, "Increase CPU to 4 vCPUs and add GPU support")
        print(f"\nUpdated configuration saved to: {updated_filepath}")
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        raise

if __name__ == "__main__":
    icl_agent()
