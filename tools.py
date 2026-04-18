from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Setup the Database Connection
db_path = "data/ecommerce.db"
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
        return f"Error: {str(e)}. Please check your table/column names and try again."
    
@tool
def get_business_rules(topic: str = None):
    """
    Returns business rules for the e-commerce store.
    Use this before writing the SQL query if the user mentions business metrics like 
    'revenue', 'VIP customers', or 'active products'.
    """
    rules = {
        "revenue": "Calculated as sum of (Products.price * Order_Items.quantity).",
        "profit": "Calculated as (revenue - (cost * quantity)), where cost is assumed to be 70% of price.",
        "vip_customer": "A customer who has spent over $500 in total.",
        "churned_customer": "A customer whose last order was more than 30 days ago.",
        "active_product": "A product that has been ordered at least once in the last 30 days."
    }
    
    if topic and topic.lower() in rules:
        return {topic: rules[topic.lower()]}
    return rules