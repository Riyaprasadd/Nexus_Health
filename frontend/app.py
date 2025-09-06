import json
import requests
import streamlit as st

# -------------------- Config --------------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Global Wellness Chatbot",
    page_icon="🌍",
    layout="wide"
)

# -------------------- Session State --------------------
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "messages" not in st.session_state:
    st.session_state.messages = []  # (role, content)
if "ui_language" not in st.session_state:
    st.session_state.ui_language = "English"  # default language

# -------------------- Sidebar --------------------
st.sidebar.title("Menu")

# Language selection
st.sidebar.subheader("Language")
ui_lang = st.sidebar.radio(
    "Choose Language",
    ["English", "Hindi"],
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state.ui_language = ui_lang

# Navigation
choice = st.sidebar.radio(
    "",
    ["Login", "Register", "Chatbot", "Reset Password"],
    label_visibility="collapsed"
)

# Logout button
if st.session_state.username:
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.session_state.messages = []
        st.rerun()

# -------------------- Helper Functions --------------------
def safe_json(response):
    """Safely parse JSON response from backend."""
    try:
        return response.json()
    except Exception:
        return {"detail": response.text or "Unknown error"}

# -------------------- Page Functions --------------------
def page_register():
    st.title("📝 Register")

    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username")
            age = st.number_input("Age", min_value=10, max_value=120, value=18)
        with col2:
            email = st.text_input("Email")
            gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")

    if submit:
        try:
            payload = {
                "username": username.strip(),
                "email": email.strip(),
                "age": int(age),
                "gender": gender,
                "password": password,
            }
            r = requests.post(f"{API_URL}/register", json=payload, timeout=15)
            if r.status_code == 200:
                data = safe_json(r)
                st.success(data.get("message", "Registered! Please login."))
            else:
                st.error(safe_json(r).get("detail", "Registration failed"))
        except Exception as e:
            st.error(f"Something went wrong. ({e})")

def page_login():
    st.title("🔐 Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        try:
            r = requests.post(
                f"{API_URL}/login",
                json={"username": username.strip(), "password": password},
                timeout=15
            )
            if r.status_code == 200:
                data = safe_json(r)
                st.session_state.username = data.get("username") or username
                st.session_state.token = "ok"  # simple logged-in flag
                st.success(data.get("message", "Login successful"))
                st.rerun()
            else:
                st.error(safe_json(r).get("detail", "Invalid credentials"))
        except Exception as e:
            st.error(f"Something went wrong. ({e})")

def page_chatbot():
    if not st.session_state.username:
        st.warning("⚠️ Please login first.")
        return

    st.title("💬 Global Wellness Chatbot")
    st.caption(
        f"Welcome, **{st.session_state.username}** | Language: **{st.session_state.ui_language}**"
    )

    # Display chat history
    for role, msg in st.session_state.messages:
        st.chat_message(role).markdown(msg)

    if user_input := st.chat_input("Ask me anything about health & wellness..."):
        # Local echo
        st.session_state.messages.append(("user", user_input))
        st.chat_message("user").markdown(user_input)

        try:
            payload = {
                "user": st.session_state.username,
                "message": user_input,
                "language": st.session_state.ui_language,
            }
            r = requests.post(f"{API_URL}/chat", json=payload, timeout=30)
            if r.status_code == 200:
                bot_reply = safe_json(r).get("response", "Something went wrong.")
            else:
                bot_reply = safe_json(r).get("detail", "Something went wrong.")
        except Exception as e:
            bot_reply = f"Error: {e}"

        st.session_state.messages.append(("assistant", bot_reply))
        st.chat_message("assistant").markdown(bot_reply)

def page_reset():
    st.title("🔧 Reset Password")
    st.info("Not implemented in this minimal demo.")

# -------------------- Router --------------------
if choice == "Register":
    page_register()
elif choice == "Login":
    page_login()
elif choice == "Chatbot":
    page_chatbot()
else:
    page_reset()
