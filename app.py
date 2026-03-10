import streamlit as st
from frontend.chat_ui import render_chat
from frontend.sidebar import render_sidebar

st.set_page_config(
    page_title="Conversational BI Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
render_sidebar()

# Main chat UI
render_chat()