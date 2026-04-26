from langchain_core.tools import tool
from db_clients import get_sql_db, get_vector_db

# Setup the SQL Database
sql_db = get_sql_db()

# Setup the Vector Database
vector_db = get_vector_db()

@tool
def list_tables():
    """
    Returns a list of all tables in the database.
    Use this to find which tables are relevant to the user's question.
    """
    try:
        return sql_db.get_usable_table_names()
    except Exception as e:
        return {"error": f"Failed to retrieve table list: {str(e)}"}

@tool
def get_schema(table_name: str):
    """
    Returns the schema and sample rows for a specific table. 
    Use this to understand column names and types before writing a SQL query.
    """
    try:
        info = sql_db.get_table_info([table_name])
        if not info:
            return {"error": f"Table '{table_name}' not found in database."}
        return info
    except Exception as e:
        return {"error": f"Error retrieving schema for '{table_name}': {str(e)}"}

@tool
def search_business_rule(query: str):
    """
    Searches for a specific business definition or formula.
    Use this to understand a business term like gross margin, revenue, profit, VIPs, churn, CLV, active products, or others.
    """
    try:
        docs_and_scores = vector_db.similarity_search_with_score(query, k=1)

        if not docs_and_scores:
            return {"message": "No relevant business rules were found."}
        
        doc, score = docs_and_scores[0]

        if score > 1.0: 
            return {"message": "No relevant business rules were found."}
        
        return doc.page_content
    
    except Exception as e:
        return {"error": f"Failed to search business rule: {str(e)}"}
    
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
        result = sql_db.run(query)
        if not result:
            return {"message": "Query executed successfully, but returned no results."}
        return result
    except Exception as e:
        return {"error": f"SQL Error: {str(e)}"}