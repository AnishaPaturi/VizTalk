import streamlit as st
import os
import json

CHAT_DIR = "saved_chats"


def render_sidebar():

    # ---------- LOGO + TITLE ----------
    st.sidebar.markdown(
        "<h2 style='color:#4CAF50;'>VizTalk</h2>",
        unsafe_allow_html=True
    )

    st.sidebar.divider()

    # ---------- SAVED CHATS ----------
    st.sidebar.subheader("Saved Chats")

    if not os.path.exists(CHAT_DIR):
        os.makedirs(CHAT_DIR)

    files = os.listdir(CHAT_DIR)

    # sort chats by creation time (newest first)
    files = sorted(
        files,
        key=lambda x: os.path.getctime(os.path.join(CHAT_DIR, x)),
        reverse=True
    )

    for file in files:

        # convert filename to readable title
        title = file.replace(".json", "").replace("_", " ").title()

        if st.sidebar.button(title):

            with open(os.path.join(CHAT_DIR, file)) as f:
                st.session_state.messages = json.load(f)

            st.rerun()

    st.sidebar.divider()

    # ---------- EXAMPLE QUERIES ----------
    st.sidebar.subheader("Example Queries")

    st.sidebar.markdown("""
    • Show revenue by region  
    • Show monthly revenue trend  
    • Show top product categories  
    """)