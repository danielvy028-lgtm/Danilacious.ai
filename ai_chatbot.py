import streamlit as st
from openai import OpenAI

# ========== SETTINGS ==========
# Put your Google Gemini API key here
API_KEY = "your_google_api_key_here"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

MODEL = "gemini-3.6-flash"   # Using Gemini 3.6 Flash
# ==============================

st.set_page_config(page_title="Gemini 3.6 Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini 3.6 Chatbot")
st.write("Ask me anything!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
            except Exception as e:
                reply = f"Error: {str(e)}"
                st.error(reply)

    # Save AI reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
