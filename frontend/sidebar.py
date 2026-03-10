import streamlit as st
import os
import json

def render_sidebar():

    # st.sidebar.title("📊 Data Controls")

    # uploaded_file = st.sidebar.file_uploader("Upload CSV Dataset")

    # if uploaded_file:
    #     st.session_state.dataset = uploaded_file
    #     st.sidebar.success("Dataset uploaded")

    # st.sidebar.divider()

    st.sidebar.subheader("Saved Chats")

    if not os.path.exists("saved_chats"):
        os.makedirs("saved_chats")

    files = os.listdir("saved_chats")

    for file in files:
        if st.sidebar.button(file):

            with open(f"saved_chats/{file}") as f:
                st.session_state.messages = json.load(f)

    st.sidebar.divider()

    st.sidebar.subheader("Example Queries")

    st.sidebar.markdown("""
    • Show revenue by region  
    • Show monthly revenue trend  
    • Show top product categories  
    """)
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.page = "landing"
        st.session_state.messages = []
        st.rerun()