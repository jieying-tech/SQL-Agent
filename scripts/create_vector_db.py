import os
import sys
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Adds the parent directory (root) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

br_doc_path = os.getenv("BUSINESS_RULES_URL", "data/business_rules.md")
br_index_path = os.getenv("BUSINESS_RULES_INDEX_URL", "data/faiss_index")

embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# Clean start
if os.path.exists(br_index_path):
    os.remove(br_index_path)

# Create index for business rules
with open(br_doc_path, "r", encoding="utf-8") as f:
    full_text = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n* ", "\n## ", "\n\n", "\n"],
    chunk_size=200,
    chunk_overlap=0
)
chunks = text_splitter.split_text(full_text)
vector_db = FAISS.from_texts(chunks, embeddings)
vector_db.save_local(br_index_path)

print("Vector database created")