# 🤖 YAML Configuration Generator

A conversational AI tool that converts natural language into Spheron Infrastructure Composition Language (ICL) YAML configurations. Say goodbye to manual YAML writing and hello to intuitive infrastructure deployment!

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-red)

## 🚀 Features

- 💬 Natural language to YAML conversion
- ✅ Built-in validation for Spheron ICL specifications
- 📝 Interactive chat-based interface
- 💾 One-click YAML downloads
- 🔄 Easy configuration refinement
- 🎨 Modern, user-friendly UI

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/yaml-config-generator.git
cd yaml-config-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API key:
```python
# In app.py, replace YOUR_API_KEY_HERE with your actual Gemini API key
genai.configure(api_key="YOUR_API_KEY_HERE")
```

## 🏃‍♂️ Running the Application

Start the application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## 📝 Usage Example

Simply describe what you want:
```
"Deploy a Node.js application with 2GB RAM and auto-scaling between 2-5 instances"
```

The tool will generate valid YAML:
```yaml
compute:
  type: "container"
  runtime: "nodejs"
  resources:
    memory: "2GB"
  scaling:
    min: 2
    max: 5
  healthCheck:
    path: "/health"
    interval: "30s"
```

## 🎯 Problem it Solves

- Eliminates the need to memorize YAML syntax
- Speeds up infrastructure configuration
- Reduces deployment errors
- Makes Spheron ICL accessible to developers of all experience levels
- Streamlines the configuration process through natural conversation

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28+
- Google Generative AI API access
- PyYAML
- PyPDF

## 🔧 Configuration

Key configuration options in `app.py`:

```python
# Generation settings
generation_config = {
    "temperature": 0.1,  # Lower for more consistent outputs
    "top_p": 0.8,
    "top_k": 40,
}

# Page configuration
st.set_page_config(
    page_title="YAML Config Generator",
    page_icon="🤖",
    layout="wide"
)
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## ✨ Acknowledgements

- [Streamlit](https://streamlit.io/) for the web interface
- [Google Generative AI](https://ai.google.dev/) for natural language processing
- [Spheron](https://spheron.network/) for ICL specifications

## 📞 Support

For support:
- Open an issue in this repository
- Contact: support@example.com
- Documentation: [Link to docs]

## 🛣️ Roadmap

- [ ] Support for more complex networking configurations
- [ ] Custom template support
- [ ] Configuration version control
- [ ] Team collaboration features
- [ ] Integration with CI/CD pipelines

---
Built with ❤️ for the Spheron community
