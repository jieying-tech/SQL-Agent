import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

def get_sql_db():
    try:
        print(f"\n--- [DB CLIENT LOG] Initializing SQL database connection ---")
        sql_db_path = os.getenv("DATABASE_URL", "data/ecommerce.db")
        engine = create_engine(f"sqlite:///file:{sql_db_path}?mode=ro&uri=true")
        return SQLDatabase(engine)
    except Exception as e:
        print(f"\n--- [DB CLIENT LOG] Error initializing SQL database connection: {str(e)} ---")
        return None

def get_vector_db():
    try:
        print(f"\n--- [DB CLIENT LOG] Initializing vector database connection ---")
        br_index_path = os.getenv("BUSINESS_RULES_INDEX_URL", "data/faiss_index")
        embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        return FAISS.load_local(br_index_path, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        print(f"\n--- [DB CLIENT LOG] Error initializing vector database connection: {str(e)} ---")
        return None