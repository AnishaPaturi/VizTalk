import streamlit as st
import requests
import pandas as pd
import os
import json
from datetime import datetime

API_URL = "http://127.0.0.1:8000/query"


# -------- SAVE CHAT --------
def save_chat(messages):

    if not os.path.exists("saved_chats"):
        os.makedirs("saved_chats")

    title = "chat"

    for msg in messages:
        if msg["role"] == "user":
            title = msg["content"][:40]
            break

    title = title.replace(" ", "_").replace("?", "")

    filename = datetime.now().strftime("%Y%m%d_%H%M%S")

    with open(f"saved_chats/{title}_{filename}.json", "w") as f:
        json.dump(messages, f)


# -------- MAIN CHAT UI --------
def render_chat():

    # -------- CHATGPT STYLE CSS --------
    st.markdown(
        """
        <style>

        .block-container {
            max-width: 900px;
            margin: auto;
        }

        .stChatMessage {
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 12px;
        }

        .stApp {
            background-color: #0E1117;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # -------- HEADER --------
    st.markdown(
        """
        <h1 style='text-align:center;'>🤖 Conversational BI Dashboard</h1>
        <p style='text-align:center;color:gray'>
        Ask business questions in natural language and instantly generate dashboards.
        </p>
        """,
        unsafe_allow_html=True
    )

    # -------- SESSION STATE --------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -------- EMPTY STATE --------
    if len(st.session_state.messages) == 0:

        st.markdown(
            """
            <div style='text-align:center;margin-top:80px;color:gray'>
            <h3>Start analyzing your data</h3>
            <p>Try asking:</p>
            <ul style='list-style:none'>
            <li>Show revenue by campaign type</li>
            <li>Show impressions by marketing channel</li>
            <li>Show click trends over time</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------- DISPLAY CHAT HISTORY --------
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.write(msg["content"])

            if "data" in msg:

                df = pd.DataFrame(msg["data"])

                if not df.empty:

                    # -------- KPI CARDS --------
                    numeric_cols = df.select_dtypes(include=["number"]).columns

                    if len(numeric_cols) > 0:

                        kpi_cols = st.columns(min(3, len(numeric_cols)))

                        for i, col in enumerate(numeric_cols[:3]):

                            value = df[col].sum()

                            kpi_cols[i].metric(
                                label=col.replace("_", " "),
                                value=f"{value:,.0f}"
                            )

                    st.dataframe(df)

                    chart = msg.get("chart")
                    x = msg.get("x")
                    y = msg.get("y")

                    if x in df.columns and y in df.columns:

                        st.subheader(f"{y} by {x}")

                        if chart == "bar":
                            st.bar_chart(df.set_index(x)[y])

                        elif chart == "line":
                            st.line_chart(df.set_index(x)[y])

                else:
                    st.warning("No data returned from this query.")

    # -------- CHAT INPUT --------
    prompt = st.chat_input("Ask a question about your data")

    if prompt:

        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # -------- FOLLOW-UP CONTEXT --------
        context = ""

        if len(st.session_state.messages) > 1:
            context = st.session_state.messages[-2]["content"]

        # -------- CALL BACKEND --------
        with st.spinner("Generating dashboard..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "prompt": prompt,
                        "context": context
                    }
                )

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

        # -------- ASSISTANT RESPONSE --------
        with st.chat_message("assistant"):

            st.code(sql)

            if df.empty:
                st.warning("No data found for this query.")
            else:

                # -------- KPI CARDS --------
                numeric_cols = df.select_dtypes(include=["number"]).columns

                if len(numeric_cols) > 0:

                    kpi_cols = st.columns(min(3, len(numeric_cols)))

                    for i, col in enumerate(numeric_cols[:3]):

                        value = df[col].sum()

                        kpi_cols[i].metric(
                            label=col.replace("_", " "),
                            value=f"{value:,.0f}"
                        )

                st.dataframe(df)

                if x in df.columns and y in df.columns:

                    st.subheader(f"{y} by {x}")

                    if chart == "bar":
                        st.bar_chart(df.set_index(x)[y])

                    elif chart == "line":
                        st.line_chart(df.set_index(x)[y])

        # -------- SAVE MESSAGE --------
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Here is the generated dashboard",
            "data": data,
            "chart": chart,
            "x": x,
            "y": y
        })

        save_chat(st.session_state.messages)