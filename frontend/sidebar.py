import streamlit as st
import os
import json
import requests

UPLOAD_API = "http://127.0.0.1:8000/upload"

def render_sidebar():

    st.sidebar.title("💬 Chats")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -------- NEW CHAT --------
    if st.sidebar.button("➕ New Chat"):
        st.session_state.messages = []

    st.sidebar.divider()

    # -------- CSV UPLOAD --------
    st.sidebar.subheader("Upload Dataset")

    uploaded_file = st.sidebar.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    if uploaded_file:

        try:

            response = requests.post(
                UPLOAD_API,
                files={"file": uploaded_file}
            )

            result = response.json()

            st.sidebar.success("Dataset uploaded!")

            st.sidebar.write("Columns:")
            st.sidebar.write(result.get("columns", []))

        except Exception as e:

            st.sidebar.error("Upload failed")
            st.sidebar.write(e)

    st.sidebar.divider()

    # -------- SAVED CHATS --------
    st.sidebar.subheader("Saved Conversations")

    if not os.path.exists("saved_chats"):
        os.makedirs("saved_chats")

    files = os.listdir("saved_chats")
    files.sort(reverse=True)

    for file in files:

        title = file.replace(".json", "").replace("_", " ")

        if st.sidebar.button(title, key=file):

            with open(f"saved_chats/{file}", "r") as f:
                st.session_state.messages = json.load(f)