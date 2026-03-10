import streamlit as st
import json
import os

from frontend.chat_ui import render_chat
from frontend.sidebar import render_sidebar

st.set_page_config(
    page_title="VizTalk",
    page_icon="favicon.png",
    layout="wide"
)

# -------- SESSION STATE --------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "user" not in st.session_state:
    st.session_state.user = None


# -------- USER STORAGE --------
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)


def load_users():
    with open(USER_FILE) as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


# -------- LANDING PAGE --------
if st.session_state.page == "landing":

    col1, col2 = st.columns([8,1])

    with col2:
        if st.button("Login / Register"):
            st.session_state.page = "login"
            st.rerun()

    st.markdown(
        "<h1 style='text-align:center;'>Conversational BI Dashboard</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='text-align:center; font-size:18px;'>
        Get insights on huge data by asking simple questions
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([3,1,3])

    with col2:
        if st.button("Get Started 🚀"):
            st.session_state.page = "chat"
            st.rerun()


# -------- LOGIN PAGE --------
elif st.session_state.page == "login":

    st.title("Login / Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    # LOGIN
    with col1:
        if st.button("Login"):
            users = load_users()

            if username in users and users[username] == password:
                st.session_state.user = username
                st.session_state.page = "chat"
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # REGISTER
    with col2:
        if st.button("Register"):
            users = load_users()

            if username in users:
                st.warning("User already exists")
            else:
                users[username] = password
                save_users(users)
                st.success("Account created! Please login.")


# -------- CHAT PAGE --------
elif st.session_state.page == "chat":

    # Sidebar visible only in chat
    render_sidebar()

    # Main chat UI
    render_chat()