import streamlit as st
import requests
from components.sidebar import show_sidebar  # ✅ Optional if using custom sidebar

# --- Config ---
st.set_page_config(page_title="Login | SQLMate", page_icon="🔐", layout="wide")

# --- Hide Default Sidebar Nav ---
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- Custom Sidebar ---
show_sidebar()

# --- Backend URL ---
BACKEND_URL = "http://127.0.0.1:8000/auth"

# --- Redirect if Already Logged In ---
if "user_id" in st.session_state:
    st.success("✅ You're already logged in!")
    st.switch_page("pages/Chat.py")

# --- Show any session message before rendering ---
if "message" in st.session_state:
    msg_type, msg_text = st.session_state.pop("message")
    if msg_type == "success":
        st.success(msg_text)
    else:
        st.error(msg_text)

# --- Mode Toggle ---
mode = st.radio("Select Action", ["Login", "Register"], horizontal=True)

# --- Login Section ---
if mode == "Login":
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            response = requests.post(f"{BACKEND_URL}/login", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                data = response.json()
                st.session_state["token"] = data.get("token", "")
                st.session_state["user_id"] = data.get("user_id", "")
                st.session_state["username"] = username
                st.success("✅ Login successful! Redirecting to Chat...")
                st.switch_page("pages/Chat.py")
            else:
                st.error(response.json().get("detail", "Invalid credentials."))

# --- Register Section ---
elif mode == "Register":
    st.title("📝 Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Register"):
        if not new_username or not new_password:
            st.error("Please enter a username and password to register.")
        else:
            response = requests.post(f"{BACKEND_URL}/register", json={
                "username": new_username,
                "password": new_password
            })
            if response.status_code == 200:
                st.session_state["message"] = ("success", "✅ Registration successful! You can now log in.")
                st.rerun()
            else:
                st.session_state["message"] = ("error", response.json().get("detail", "User already exists."))
                st.rerun()
