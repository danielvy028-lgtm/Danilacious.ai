import os
import streamlit as st
from google import genai
from google.genai import types

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="Danilacious AI",
    page_icon="🍵",
    layout="centered"
)

# -------------------------
# Load API Key
# -------------------------
API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# -------------------------
# System Prompt
# -------------------------
SYSTEM_PROMPT = """
You are a friendly and helpful assistant for Danilacious.
Created by Airaodion Daniel.

Key information:
- Location: 57, Dan Vile Estates, Lagos
- WhatsApp: 09033116420
- WhatsApp link: https://wa.me/2349033116420
- Instagram & TikTok: @danilacious
- Signature drinks: Iced Matcha Latte
- Prices: Matcha from ₦3,500
- Sometimes we have 10% OFF promotions

Be warm, polite and helpful. Keep answers short and natural.
If someone wants to order, tell them to message us on WhatsApp.
"""

# -------------------------
# Initialize chat history
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# UI
# -------------------------
st.title("🍵 Danilacious AI")
st.caption("Your friendly Matcha assistant")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about Danilacious..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                history = [
                    types.Content(
                        role="user" if m["role"] == "user" else "model",
                        parts=[types.Part(text=m["content"])]
                    )
                    for m in st.session_state.messages[:-1]
                ]

                chat = client.chats.create(
                    model="gemini-3.6-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    ),
                    history=history
                )

                response = chat.send_message(prompt)
                answer = response.text

            except Exception as e:
                answer = f"Sorry, something went wrong: {str(e)}"

            st.markdown(answer)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": answer})
