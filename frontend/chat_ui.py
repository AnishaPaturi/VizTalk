import streamlit as st

def render_chat():

    # # Dataset controls near input
    # with st.container():
    #     st.markdown("### 📊 Data Controls")

    #     uploaded_file = st.file_uploader("Upload CSV Dataset")

    #     if uploaded_file:
    #         st.session_state.dataset = uploaded_file
    #         st.success("Dataset uploaded")

    #     st.divider()


    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


    # Chat input
    prompt = st.chat_input("Ask a question about your data")

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })