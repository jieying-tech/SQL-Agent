import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import json

# Load environment variables
load_dotenv()

# Setup the Database Connection
db_path = os.getenv("DATABASE_URL")
engine = create_engine(f"sqlite:///file:{db_path}?mode=ro&uri=true")
db = SQLDatabase(engine)

@tool
def list_tables():
    """
    Returns a list of all tables in the database.
    Use this to find which tables are relevant to the user's question.
    """
    try:
        return db.get_usable_table_names()
    except Exception as e:
        return {"error": f"Failed to retrieve table list: {str(e)}"}

@tool
def get_schema(table_name: str):
    """
    Returns the schema and sample rows for a specific table. 
    Use this to understand column names and types before writing a SQL query.
    """
    try:
        info = db.get_table_info([table_name])
        if not info:
            return {"error": f"Table '{table_name}' not found in database."}
        return info
    except Exception as e:
        return {"error": f"Error retrieving schema for '{table_name}': {str(e)}"}

@tool
def execute_query(query: str):
    """
    Executes a SQL query against the database and returns the results.
    If the query fails, it returns the error message. Use the error to fix your query.
    """
    query_upper = query.upper()

    # Reject forbidden keywords
    forbidden_keywords = ["DROP", "TRUNCATE", "DELETE", "UPDATE", "INSERT", "ALTER"]
    if any(word in query_upper for word in forbidden_keywords):
        return {"error": "Forbidden keyword detected. Only SELECT queries are allowed."}
    
    # Reject SELECT *
    if "SELECT *" in query_upper:
        return {"error": "SELECT * is disabled for performance. Please specify column names explicitly."}
    
    # Inject LIMIT if missing
    if "SELECT" in query_upper and "LIMIT" not in query_upper:
        query = query.rstrip(';') + " LIMIT 50;"

    try:
        result = db.run(query)
        if not result:
            return {"message": "Query executed successfully, but returned no results."}
        return result
    except Exception as e:
        return {"error": f"SQL Error: {str(e)}"}
    
@tool
def get_business_rules():
    """
    Returns business definitions and formulas.
    Use this to understand the business rules for metrics like revenue, profit, VIPs, churn, and active products.
    """
    try:
        with open("data/business_rules.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Business rules file not found."}