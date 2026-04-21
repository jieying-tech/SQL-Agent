import sys
import os
import pytest

# Adds the parent directory (root) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools import execute_query


### Test 1: Successful query with data returned

def test_execute_query_returns_data():
    query = "SELECT product_id, name, price, category FROM Products LIMIT 1;"
    result = execute_query.invoke({"query": query})
    assert isinstance(result, str)
    assert "error" not in result
    assert "returned no results" not in result


### Test 2: Successful query with no data returned

def test_execute_query_returns_no_data():
    query = "SELECT customer_id FROM Orders WHERE order_id = -999;"
    result = execute_query.invoke({"query": query})
    assert "message" in result
    assert "returned no results" in result["message"]


### Test 3: Forbidden commands

@pytest.mark.parametrize("forbidden_query", [
    "DROP TABLE Orders;",
    "TRUNCATE TABLE Logs;",
    "DELETE FROM Products;"
    "UPDATE Customers SET name = 'Hacked';",
    "INSERT INTO Products (name) VALUES ('Ghost');",
    "ALTER TABLE Users ADD COLUMN password TEXT;",
])
def test_execute_query_forbidden_commands(forbidden_query):
    result = execute_query.invoke({"query": forbidden_query})
    assert isinstance(result, dict)
    assert "error" in result
    assert "Forbidden keyword detected" in result["error"]


### Test 4: Incorrect table or column name

def test_execute_query_incorrect_table():
    query = "SELECT customer_id FROM NonExistentTable"
    result = execute_query.invoke({"query": query})
    assert "error" in result
    assert "no such table" in result["error"]

def test_execute_query_incorrect_column():
    query = "SELECT NonExistentColumn FROM Customers"
    result = execute_query.invoke({"query": query})
    assert "error" in result
    assert "no such column" in result["error"]