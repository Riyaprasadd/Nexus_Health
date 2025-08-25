# frontend/app.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"  # backend endpoint

st.set_page_config(page_title="Global Wellness Chatbot", page_icon="🌍", layout="wide")

# ---- Header ----
st.title("🌍 Global Wellness Chatbot")
st.caption("Your personal AI companion for **health & wellness guidance** 🧘🍎")

# ---- Sidebar (actions & tips) ----
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("Clear conversation"):
        st.session_state.pop("messages", None)
        st.rerun()

    st.markdown("### ℹ️ Notes")
    st.markdown(
        "- Educational info only — not medical advice.\n"
        "- For emergencies, contact local emergency services."
    )

# ---- Chat state ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me anything about health & wellness."}
    ]

# ---- Render history ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- User input ----
if prompt := st.chat_input("Ask me about sleep, nutrition, stress, diabetes, etc."):
    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                r = requests.post(API_URL, json={"message": prompt}, timeout=60)
                r.raise_for_status()
                bot_reply = r.json().get("reply") or "Sorry, I couldn't find an answer."
            except Exception as e:
                bot_reply = f"Backend error: {e}"

            st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
