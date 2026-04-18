from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from tools import list_tables, get_schema, execute_query, get_business_rules

load_dotenv()

# 1. Define the state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Initialize the LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0
)

# 3. Bind tools
tools = [list_tables, get_schema, execute_query, get_business_rules]
llm_with_tools = llm.bind_tools(tools)

# 4. Define the system prompt
SYSTEM_PROMPT = """
    You are a Sales Analyst of an e-commerce store.
    Given an input, create a syntactically correct {dialect} query to run,
    then look at the results of the query and return the answer. Unless the user
    specifies a specific number of records they wish to obtain, always limit your
    query to at most {top_k} results.
    You have READ-ONLY access to the database. Do not attempt to modify data.
    Always format currency with a '$' prefix and 2 decimal places.
    If a business rule is used, show it in your final answer.
    
    """.format(
        dialect="SQLite",
        top_k=10,
    )

# 5. Define the reasoning engine
def call_model(state: State):
    """Processes the current conversation state and determines the next action."""
    messages = [("system", SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 6. Build the workflow
workflow = StateGraph(State)

# Define the nodes for reasoning and action
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Set the starting point of execution
workflow.set_entry_point("agent")

# Define the logic for the loop
def should_continue(state: State):
    """Determines if the agent should keep using tools or give a final answer."""
    last_message = state["messages"][-1]
    # If the LLM requests a tool, route to the action node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, terminate the workflow
    return END

# Define the iterative feedback loop
workflow.add_conditional_edges("agent", should_continue)
# Return tool results to the agent for analysis
workflow.add_edge("tools", "agent")

# 7. Compile the workflow
app = workflow.compile()