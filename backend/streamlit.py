import streamlit as st
import asyncio
from core.chatbot import MeridianChatbot

st.set_page_config(page_title="Meridian Support AI", page_icon="💻")

st.title("Meridian Electronics Support")
st.caption("AI-Powered Customer Service Prototype")

# Initialize Chatbot session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = MeridianChatbot()
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Use asyncio to run the async chatbot handler
        response = asyncio.run(st.session_state.chatbot.handle_message(prompt))
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})