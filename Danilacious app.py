import os
import gradio as gr
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are a friendly and helpful assistant for Danilacious, a premium coffee and matcha shop in Lagos, Nigeria.
Created by Airaodion Daniel.

Key information:
- Location: 57, Dan Vile Estates, Lagos, Nigeria
- WhatsApp: 09033116420
- WhatsApp link: https://wa.me/2349033116420
- Facebook: https://www.facebook.com/share/1S2VMgMrsr/
- Instagram & TikTok: @danilacious
- Signature drinks: Iced Matcha Latte, Iced Americano, Signature Latte
- Prices: Matcha from ₦3,500 | Americano from ₦2,800 | Latte from ₦3,200
- Sometimes we have 10% OFF promotions

Be warm, polite and helpful. Keep answers short and clear.
If someone wants to order, tell them to message WhatsApp.
"""

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT
    )
)

def respond(message, history):
    if not message or not message.strip():
        return history

    try:
        response = chat.send_message(message)
        bot_reply = response.text.strip() if response.text else "Sorry, I didn't get a reply. Please try again."
    except Exception as e:
        bot_reply = "Sorry, something went wrong. Please try again later."

    history.append((message, bot_reply))
    return history

with gr.Blocks(title="Danilacious AI Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# ☕ Danilacious AI Assistant 💚")
    gr.Markdown("Ask me anything about our coffee, matcha, location, prices or promotions!")
    
    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(placeholder="Type your message here...", label="Your message")
    clear = gr.Button("Clear Chat")

    msg.submit(respond, [msg, chatbot], [chatbot]).then(lambda: "", None, msg)
    clear.click(lambda: [], None, chatbot, queue=False)

demo.launch(server_name="0.0.0.0", server_port=7860
