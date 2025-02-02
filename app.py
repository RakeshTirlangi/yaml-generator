import streamlit as st
import yaml
from pypdf import PdfReader
import google.generativeai as genai
import os
from datetime import datetime
from typing import Dict, Tuple
import re
import base64


st.set_page_config(
    page_title="YAML Config Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: blue;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .yaml-output {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
    }
    .success-message {
        padding: 1rem;
        background-color: #DFF2BF;
        color: #4F8A10;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #FFE8E6;
        color: #D8000C;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #E3F2FD;
    }
    .bot-message {
        background-color: #F5F5F5;
    }
    .download-button {
        display: inline-block;
        padding: 0.5rem 1rem;
        background-color: #4CAF50;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .download-button:hover {
        background-color: #45a049;
    }
    .sidebar .decoration {
        margin-top: 20px;
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitICLAgent:
    def __init__(self):
        """Initialize the ICL Agent with predefined API key."""
        self.knowledge = {
            "schema": {"components": [], "parameters": []},
            "rules": {"validation": [], "security": []},
            "practices": {"deployment": [], "configuration": []},
            "patterns": {"common": [], "recommended": []}
        }
        # Configure Gemini API with predefined key
        genai.configure(api_key="AIzaSyDVs789LPRED3rqh2CCJpAGHuzCVoVYu1Q")  # Replace with your actual API key
        generation_config = {
            "temperature": 0.1,
            "top_p": 0.8,
            "top_k": 40,
        }
        self.model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)

    def _clean_response(self, text: str) -> str:
        """Cleans model response to ensure valid YAML formatting."""
        if not text:
            return ""
        text = re.sub(r'```[yamlYAML]*\n', '', text)
        text = text.replace('```', '')
        text = re.sub(r'#.*$', '', text, flags=re.MULTILINE)
        lines = text.strip().splitlines()
        cleaned_lines = [line.replace('\t', '  ') for line in lines if line.strip()]
        return '\n'.join(cleaned_lines)

    def _parse_yaml_safely(self, content: str) -> Dict:
        """Safely parses YAML content."""
        try:
            docs = list(yaml.safe_load_all(content))
            if not docs:
                raise ValueError("Empty YAML content")
            return docs[0] if len(docs) == 1 else {"documents": docs}
        except yaml.YAMLError as e:
            st.error(f"YAML parsing failed: {str(e)}")
            return {"error": "Failed to parse YAML", "timestamp": str(datetime.now())}

    def process_request(self, user_input: str) -> Dict:
        """Generates YAML configuration based on user input."""
        try:
            prompt = f"""
            Generate a YAML configuration based on this request: {user_input}

            Knowledge base:
            {yaml.dump(self.knowledge, default_flow_style=False)}

            Requirements:
            - Output **only valid YAML**, without markdown or extra text
            - Ensure all necessary components are included
            - Follow security and best practices
            - Use proper indentation

            Response must be **pure YAML** with no extra formatting.
            """
            
            response = self.model.generate_content(prompt)
            return self._parse_yaml_safely(self._clean_response(response.text))
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")
            return {"error": str(e)}

def get_yaml_download_link(yaml_data: Dict, filename: str = "config.yaml") -> str:
    """Generate a download link for YAML data."""
    try:
        yaml_str = yaml.dump(yaml_data, default_flow_style=False)
        b64 = base64.b64encode(yaml_str.encode()).decode()
        return f'<a href="data:file/yaml;base64,{b64}" download="{filename}" class="download-button">📥 Download YAML</a>'
    except Exception as e:
        st.error(f"Error generating download link: {str(e)}")
        return ""

def main():
    st.title("🤖 YAML Configuration Generator")
    
   
    if 'agent' not in st.session_state:
        st.session_state.agent = StreamlitICLAgent()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    
    with st.sidebar:
        st.header("💡 Tips")
        st.markdown("""
        - Be specific about your configuration needs
        - Include all necessary parameters
        - Mention any specific requirements
        - Use clear, concise language
        """)
        
        st.markdown("""
        <div class="decoration">
            🔧 Examples:
            <ul>
                <li>Deploy a Node.js app with auto-scaling</li>
                <li>Configure a Redis cache with 2GB memory</li>
                <li>Set up a PostgreSQL database with replication</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    
    user_input = st.text_area("💭 What configuration would you like to generate?", height=100)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 Generate Configuration"):
            if user_input:
                
                st.session_state.chat_history.append(("user", user_input))
                
                
                with st.spinner("🔄 Generating configuration..."):
                    config = st.session_state.agent.process_request(user_input)
                
                
                yaml_str = yaml.dump(config, default_flow_style=False)
                st.session_state.chat_history.append(("bot", yaml_str))
                
                
                download_link = get_yaml_download_link(config)
                st.session_state.chat_history.append(("download", download_link))

    for msg_type, message in st.session_state.chat_history:
        if msg_type == "user":
            st.markdown(f'<div class="chat-message user-message">👤 You: {message}</div>', unsafe_allow_html=True)
        elif msg_type == "bot":
            st.markdown(f'<div class="chat-message bot-message">🤖 Generated YAML Configuration:</div>', unsafe_allow_html=True)
            st.code(message, language="yaml")
        elif msg_type == "download":
            st.markdown(message, unsafe_allow_html=True)

if __name__ == "__main__":
    main()