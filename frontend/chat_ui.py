import streamlit as st
import streamlit.components.v1 as components
import os
import json
import requests
import pandas as pd

CHAT_DIR = "saved_chats"
API_URL = "http://127.0.0.1:8000/query"


# ---------- SAVE CHAT FUNCTION ----------
def save_chat():

    if not os.path.exists(CHAT_DIR):
        os.makedirs(CHAT_DIR)

    # create file when first message appears
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

        # prevent overwriting chats
        counter = 1
        while os.path.exists(filename):
            filename = f"{CHAT_DIR}/{title}_{counter}.json"
            counter += 1

        st.session_state.current_chat_file = filename

    # save conversation
    with open(st.session_state.current_chat_file, "w") as f:
        json.dump(st.session_state.messages, f, indent=2)


def render_chat():

    # ---------- SESSION STATE ----------
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

    with right:
        components.html(
        """
        <div id="voice-container">
            <button id="voice-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
            <path d="M12 15a3 3 0 003-3V5a3 3 0 10-6 0v7a3 3 0 003 3zm5-3a1 1 0 10-2 0 3 3 0 11-6 0 1 1 0 10-2 0 5 5 0 004 4.9V21H9a1 1 0 100 2h6a1 1 0 100-2h-2v-2.1A5 5 0 0017 12z"/>
            </svg>
            </button>
            <span id="voice-status"></span>
        </div>

        <script>
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();

            recognition.lang = "en-US";
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            let isRecording = false;

            const btn = document.getElementById("voice-btn");
            const status = document.getElementById("voice-status");

            btn.onclick = () => {

                if (!isRecording) {
                    recognition.start();
                    isRecording = true;
                    status.innerText = "Listening...";
                    btn.innerHTML = "⏹";
                } 
                else {
                    recognition.stop();
                    isRecording = false;
                    status.innerText = "";
                    btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="white">
                    <path d="M12 15a3 3 0 003-3V5a3 3 0 10-6 0v7a3 3 0 003 3zm5-3a1 1 0 10-2 0 3 3 0 11-6 0 1 1 0 10-2 0 5 5 0 004 4.9V21H9a1 1 0 100 2h6a1 1 0 100-2h-2v-2.1A5 5 0 0017 12z"/>
                    </svg>`;
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
                isRecording = false;
                status.innerText = "";
            };

            recognition.onerror = function(){
                isRecording = false;
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
            font-size:18px;
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

    st.title("🤖 Conversational BI Dashboard")

    st.markdown("""
    Ask business questions in natural language and instantly generate dashboards.

    Example queries:

    - Show revenue by campaign type
    - Show revenue trend by date
    - Show top marketing channels
    """)

    # ---------- DISPLAY CHAT ----------
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.write(msg["content"])

            if "data" in msg:

                df = pd.DataFrame(msg["data"])
                st.dataframe(df)

                chart = msg.get("chart")
                x = msg.get("x")
                y = msg.get("y")

                if x in df.columns and y in df.columns:

                    if chart == "bar":
                        st.bar_chart(df.set_index(x)[y])

                    elif chart == "line":
                        st.line_chart(df.set_index(x)[y])

                    elif chart == "pie":
                        st.write(df)

    # ---------- CHAT INPUT ----------
    prompt = st.chat_input("Ask a question about your data")

    if prompt:

        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        save_chat()

        # ---------- BACKEND QUERY ----------
        with st.spinner("Processing your request..."):

            try:
                response = requests.post(
                    API_URL,
                    json={"prompt": prompt},
                    timeout=60
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

        save_chat()