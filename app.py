import streamlit as st
from frontend.chat_ui import render_chat
from frontend.sidebar import render_sidebar

st.set_page_config(
    page_title="VizTalk",
    page_icon="favicon.png",
    layout="wide"
)

# session state for new chat
if "new_chat" not in st.session_state:
    st.session_state.new_chat = False

def handle_js_events():
    if st.session_state.get("new_chat_event"):
        st.session_state.new_chat = True
        st.session_state.new_chat_event = False

# Sidebar
render_sidebar()

# Main chat UI
render_chat()