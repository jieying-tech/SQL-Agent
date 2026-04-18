import streamlit as st
from agent import app

st.set_page_config(page_title="SQL Agent", page_icon="🎵")

st.title("SQL Agent")
st.markdown("Ask me anything about the e-commerce data.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Which product has the highest number of orders?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Thinking and Querying Database..."):
            inputs = {"messages": [("user", prompt)]}
            result = app.invoke(inputs)

            with st.expander("🔍 Show Agent Thought Process"):
                # Skip the first message (the user prompt) and the last (final answer)
                process_messages = result["messages"][1:-1]
                
                for msg in process_messages:
                    # Show what actions the agent decided to take (Tool Calls)
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            st.write(f"**Step:** Agent decided to use `{tool_call['name']}`")
                            if "query" in tool_call["args"]:
                                st.code(tool_call["args"]["query"], language="sql")
                            elif "table_name" in tool_call["args"]:
                                st.write(f"Inspecting table: `{tool_call['args']['table_name']}`")
                    
                    # Show the raw result from the database (Tool Messages)
                    elif msg.type == "tool":
                        st.caption("Data retrieved from database:")
                        # Truncate long results for UI cleanliness
                        content = str(msg.content)
                        st.text(content[:300] + "..." if len(content) > 300 else content)

            # Extract the final response
            final_message = result["messages"][-1]
            full_response = final_message.content
            
        # Display the final response
        message_placeholder.markdown(full_response)
    
    # Persist the assistant's response to the session history
    st.session_state.messages.append({"role": "assistant", "content": final_message})