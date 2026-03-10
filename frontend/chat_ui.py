import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/query"

def render_chat():

    st.title("🤖 Conversational BI Dashboard")

    st.markdown("""
Ask business questions in natural language and instantly generate dashboards.

Example queries:

- Show revenue by campaign type
- Show revenue trend by date
- Show top marketing channels
""")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

            if "data" in msg and msg["data"]:
                df = pd.DataFrame(msg["data"])
                st.dataframe(df)

                chart = msg.get("chart")
                x = msg.get("x")
                y = msg.get("y")

                if x in df.columns and y in df.columns:

                    if chart == "bar":
                        st.subheader("Bar Chart")
                        st.bar_chart(df.set_index(x)[y])

                    elif chart == "line":
                        st.subheader("Trend Analysis")
                        st.line_chart(df.set_index(x)[y])

                    elif chart == "pie":
                        st.subheader("Distribution")
                        st.write(df)

    # Chat input
    prompt = st.chat_input("Ask a question about your data")

    if prompt:

        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.spinner("Generating dashboard..."):

            try:
                response = requests.post(
                    API_URL,
                    json={"prompt": prompt},
                    timeout=60
                )

                if response.status_code != 200:
                    st.error("Backend error.")
                    return

                result = response.json()

                sql = result.get("sql")
                data = result.get("data")
                chart = result.get("chart")
                x = result.get("x")
                y = result.get("y")

                df = pd.DataFrame(data)

            except Exception as e:
                st.error(f"Backend error: {e}")
                return

        with st.chat_message("assistant"):

            st.write("Generated SQL:")
            st.code(sql)

            st.write("Query Result")
            st.dataframe(df)

            if x in df.columns and y in df.columns:

                if chart == "bar":
                    st.bar_chart(df.set_index(x)[y])

                elif chart == "line":
                    st.line_chart(df.set_index(x)[y])

                elif chart == "pie":
                    st.write(df)

        st.session_state.messages.append({
            "role": "assistant",
            "content": "Here is the generated dashboard",
            "data": data,
            "chart": chart,
            "x": x,
            "y": y
        })