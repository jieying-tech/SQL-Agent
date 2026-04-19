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
    return db.get_usable_table_names()

@tool
def get_schema(table_name: str):
    """
    Returns the schema and sample rows for a specific table. 
    Use this to understand column names and types before writing a SQL query.
    """
    return db.get_table_info([table_name])

@tool
def execute_query(query: str):
    """
    Executes a SQL query against the database and returns the results.
    If the query fails, it returns the error message. Use the error to fix your query.
    """
    # Define forbidden keywords
    forbidden_keywords = ["DROP", "TRUNCATE", "DELETE", "UPDATE", "INSERT", "ALTER"]
    query_upper = query.upper()

    if any(word in query_upper for word in forbidden_keywords):
        return "Error: Forbidden keyword detected. Only SELECT queries are allowed."

    try:
        result = db.run(query)
        if not result:
            return "Query executed successfully, but returned no results."
        return result
    except Exception as e:
        return f"Error: {str(e)}."
    
@tool
def get_business_rules():
    """
    Returns business definitions and formulas.
    Use this to understand the business rules for metrics like revenue, profit, VIPs, churn, and active products.
    """
    try:
        with open("business_rules.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Business rules file not found."}