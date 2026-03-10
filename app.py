import streamlit as st
from frontend.chat_ui import render_chat
from frontend.sidebar import render_sidebar

# Sidebar
render_sidebar()

# Main chat UI
render_chat()