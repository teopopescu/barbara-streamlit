from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st
import os

st.title("🧪 Barbara 🔬")

# Initialize the LangChain chat model
llm = ChatOpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
    model_name="meta-llama/Meta-Llama-3.1-70B-Instruct",
    streaming=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)

if prompt := st.chat_input("How can I help you today?"):
    # Add user message to state and display it
    user_message = HumanMessage(content=prompt)
    st.session_state.messages.append(user_message)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_history = st.session_state.messages
        
        # Create the streaming response placeholder
        response_placeholder = st.empty()
        accumulated_response = ""
        
        # Stream the response
        for chunk in llm.stream(message_history):
            content = chunk.content
            accumulated_response += content
            response_placeholder.markdown(accumulated_response + "▌")
        
        # Display final response without cursor
        response_placeholder.markdown(accumulated_response)
        
        # Add assistant message to state
        assistant_message = AIMessage(content=accumulated_response)
        st.session_state.messages.append(assistant_message)