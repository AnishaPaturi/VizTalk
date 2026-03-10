import streamlit as st
from frontend.sidebar import render_sidebar
from frontend.chat_ui import render_chat

st.set_page_config(layout="wide")

render_sidebar()
render_chat()