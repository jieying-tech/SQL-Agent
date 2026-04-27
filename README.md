<div align="center">
  <h2 align="center">LLM-Powered SQL Agent with RAG</h2>
  <p align="center">
    An AI agent for natural language-to-SQL generation with RAG capabilities
  </p>
</div>

<h3 id="about-the-project">About the Project</h3>
An LLM-powered AI agent that combines SQL database querying with RAG-based business rule retrieval to deliver accurate, context-aware insights through an interactive web app.

<h4 id="demo">Demo</h4>

Live app: https://sql-agent-app-tm0ynq.streamlit.app/

<h4 id="built-with">Built with</h4>

* [LangChain](https://www.langchain.com/)
* [LangGraph](https://www.langchain.com/langgraph)
* [FastEmbed](https://github.com/qdrant/fastembed)
* [Faiss](https://github.com/facebookresearch/faiss)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Streamlit](https://streamlit.io/)

<h3 id="prerequisites">Prerequisites</h3>

* [Python](https://www.python.org/)
* [Ollama](https://ollama.com/)
* [Groq API key](https://console.groq.com/home)
* [Hugging Face API key](https://huggingface.co/)
* [OpenRouter API key](https://openrouter.ai/)

<h3 id="setup">Setup</h3>

1. Install the python packages:
```sh
pip install -r requirements.txt
```
2. Create a `.env` file in the root directory of the project:
```env
# Data Paths
DATABASE_URL="data/ecommerce.db"
BUSINESS_RULES_URL="data/business_rules.md"
BUSINESS_RULES_INDEX_URL="data/faiss_index"

# Agent Settings
MAX_CONTEXT_MESSAGES=3
RECURSION_LIMIT=25

# Model Providers
AVAILABLE_MODEL_PROVIDERS="OLLAMA,GROQ,HUGGINGFACE,OPENROUTER"
MODEL_PROVIDER="OLLAMA"

# GROQ
GROQ_API_KEY=""
GROQ_MODEL_NAME="llama-3.3-70b-versatile"

# HUGGINGFACE
HUGGINGFACEHUB_API_TOKEN=""
HUGGINGFACE_MODEL_NAME="deepseek-ai/DeepSeek-V3"
HUGGINGFACE_BASE_URL="https://router.huggingface.co/v1"

# OPENROUTER
OPENROUTER_API_KEY=""
OPENROUTER_MODEL_NAME="openai/gpt-oss-120b:free"
OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"

# OLLAMA
OLLAMA_MODEL_NAME="qwen3.5:9b"
OLLAMA_BASE_URL="http://localhost:11434"
```

<h3 id="usage">Usage</h3>

1. Run the streamlit app:
  ```sh
  streamlit run app.py
  ```

2. Open the app with a browser at [localhost:8501](http://localhost:8501)