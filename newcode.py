import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("PROD_WEBHOOK_URL")

st.set_page_config(page_title="Company QA Bot", layout="centered")

# Generate stable conversation id per session (but NOT storing chat messages)
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

st.title("🤖 Company QA Assistant (Context stored in n8n)")

# Display previous conversation UI only visually (not used for logic)
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

# Render chat bubbles
for msg in st.session_state.chat_display:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message
    st.chat_message("user").write(user_input)
    st.session_state.chat_display.append({"role":"user","content":user_input})

    payload = {
        "message": user_input,
        "conversation_id": st.session_state.conversation_id
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=20)
        result = response.json()

        # Handle list or direct object
        if isinstance(result, list) and len(result) > 0:
            result = result[0]

        ai_reply = result.get("output", "⚠️ No output returned.")

        # Display assistant reply
        with st.chat_message("assistant"):
            st.write(ai_reply)
        st.session_state.chat_display.append({"role":"assistant","content":ai_reply})

    except Exception as e:
        st.chat_message("assistant").write(f"⚠️ Error: {e}")

