import streamlit as st
import streamlit.components.v1 as components
import os
import json
import requests
import pandas as pd

CHAT_DIR = "saved_chats"
API_URL = "http://127.0.0.1:8000/query"


# ---------- SAVE CHAT ----------
def save_chat():

    if not os.path.exists(CHAT_DIR):
        os.makedirs(CHAT_DIR)

    if st.session_state.current_chat_file is None:

        first_msg = None
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                first_msg = msg["content"]
                break

        if first_msg:
            words = first_msg.split()[:3]
            title = "_".join(words).lower()
        else:
            title = "chat"

        filename = f"{CHAT_DIR}/{title}.json"

        counter = 1
        while os.path.exists(filename):
            filename = f"{CHAT_DIR}/{title}_{counter}.json"
            counter += 1

        st.session_state.current_chat_file = filename

    with open(st.session_state.current_chat_file, "w") as f:
        json.dump(st.session_state.messages, f, indent=2)


# ---------- TEXT TO SPEECH ----------
def speak(text):

    components.html(
        f"""
        <script>
        const msg = new SpeechSynthesisUtterance("{text}");
        msg.rate = 1;
        msg.pitch = 1;
        msg.lang = "en-US";
        window.speechSynthesis.speak(msg);
        </script>
        """,
        height=0,
    )


def render_chat():

    # ---------- SESSION ----------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_chat_file" not in st.session_state:
        st.session_state.current_chat_file = None

    # ---------- TOP CONTROLS ----------
    left, right = st.columns([8,2])

    with left:
        if st.button("➕ New Chat"):
            st.session_state.messages = []
            st.session_state.current_chat_file = None
            st.rerun()

    # ---------- VOICE INPUT ----------
    with right:
        components.html(
        """
        <div id="voice-container">
            <button id="voice-btn">🎤</button>
            <span id="voice-status"></span>
        </div>

        <script>
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        recognition.lang = "en-US";
        recognition.interimResults = false;

        let recording = false;

        const btn = document.getElementById("voice-btn");
        const status = document.getElementById("voice-status");

        btn.onclick = () => {

            if(!recording){
                recognition.start();
                recording = true;
                status.innerText = "Listening...";
            }
            else{
                recognition.stop();
                recording = false;
                status.innerText = "";
            }
        };

        recognition.onresult = function(event){

            const text = event.results[0][0].transcript;

            const textarea = window.parent.document.querySelector("textarea");

            if(textarea){
                textarea.value = text;
                textarea.dispatchEvent(new Event("input",{bubbles:true}));
            }
        };

        recognition.onend = function(){
            recording = false;
            status.innerText = "";
        };

        recognition.onerror = function(){
            recording = false;
            status.innerText = "Mic error";
        };

        </script>

        <style>

        #voice-container{
            display:flex;
            justify-content:flex-end;
            align-items:center;
            gap:8px;
        }

        #voice-btn{
            padding:6px 10px;
            border-radius:8px;
            border:none;
            background:#262730;
            color:white;
            cursor:pointer;
        }

        #voice-btn:hover{
            background:#3a3b47;
        }

        #voice-status{
            color:#aaa;
            font-size:12px;
        }

        </style>
        """,
        height=60
        )

    # ---------- HEADER ----------
    st.title("🤖 VizTalk")

    st.markdown("""
Ask business questions in natural language and instantly generate dashboards.

Example queries:

• Show revenue by campaign type  
• Show revenue trend by date  
• Show top marketing channels  
""")

    # ---------- DISPLAY CHAT ----------
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.write(msg["content"])

            if "data" in msg:

                df = pd.DataFrame(msg["data"])

                if not df.empty:

                    numeric_cols = df.select_dtypes(include=["number"]).columns

                    if len(numeric_cols) > 0:

                        kpi_cols = st.columns(min(3, len(numeric_cols)))

                        for i, col in enumerate(numeric_cols[:3]):

                            value = df[col].sum()

                            kpi_cols[i].metric(
                                label=col.replace("_"," "),
                                value=f"{value:,.0f}"
                            )

                    st.dataframe(df)

                    chart = msg.get("chart")
                    x = msg.get("x")
                    y = msg.get("y")

                    if x in df.columns and y in df.columns:

                        if chart == "bar":
                            st.bar_chart(df.set_index(x)[y])

                        elif chart == "line":
                            st.line_chart(df.set_index(x)[y])

    # ---------- CHAT INPUT ----------
    prompt = st.chat_input("Ask a question about your data")

    if prompt:

        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({
            "role":"user",
            "content":prompt
        })

        save_chat()

        # ---------- CALL BACKEND ----------
        with st.spinner("Generating dashboard..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"prompt":prompt}
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

        # ---------- ASSISTANT RESPONSE ----------
        with st.chat_message("assistant"):

            st.code(sql)

            if df.empty:

                st.warning("No data found for this query.")
                speak("No data found for this query.")

            else:

                numeric_cols = df.select_dtypes(include=["number"]).columns

                if len(numeric_cols) > 0:

                    kpi_cols = st.columns(min(3, len(numeric_cols)))

                    for i, col in enumerate(numeric_cols[:3]):

                        value = df[col].sum()

                        kpi_cols[i].metric(
                            label=col.replace("_"," "),
                            value=f"{value:,.0f}"
                        )

                st.dataframe(df)

                if x in df.columns and y in df.columns:

                    st.subheader(f"{y} by {x}")

                    if chart == "bar":
                        st.bar_chart(df.set_index(x)[y])

                    elif chart == "line":
                        st.line_chart(df.set_index(x)[y])

                speak(f"The dashboard shows {y} by {x}")

        st.session_state.messages.append({
            "role":"assistant",
            "content":"Here is the generated dashboard",
            "data":data,
            "chart":chart,
            "x":x,
            "y":y
        })

        save_chat()