import streamlit as st
import streamlit.components.v1 as components
import os
import json
import requests
import pandas as pd
import random

CHAT_DIR = "saved_chats"
API_URL = "http://127.0.0.1:8000/query"


# ---------- AUTO VOICE ----------
def auto_speak(text):

    safe_text = text.replace('"', "'")

    components.html(
        f"""
        <script>
        const msg = new SpeechSynthesisUtterance("{safe_text}");
        msg.rate = 1;
        msg.pitch = 1;
        msg.lang = "en-US";

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
        </script>
        """,
        height=0,
    )


# ---------- GENERATE INSIGHTS ----------
def generate_insight(df, x, y):

    if df.empty or x not in df.columns or y not in df.columns:
        return ["I generated your dashboard."]

    insights = []

    try:

        top_row = df.sort_values(by=y, ascending=False).iloc[0]
        bottom_row = df.sort_values(by=y, ascending=True).iloc[0]

        insights.append(
            f"{top_row[x]} has the highest {y} with a value of {top_row[y]}."
        )

        insights.append(
            f"{bottom_row[x]} has the lowest {y} with a value of {bottom_row[y]}."
        )

        insights.append(
            f"This chart compares {y} across different {x} categories."
        )

    except Exception:
        insights.append(f"The dashboard shows {y} grouped by {x}.")

    return insights


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


# ---------- MAIN CHAT ----------
def render_chat():
    username = st.session_state.get("user")
    if username:
        st.markdown(f"""
        ### Hello, **{username}** 👋  
        How can I help you?
        """)
    else:
        st.markdown("""
        ### Hello 👋  
        How can I help you today?
        """)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_chat_file" not in st.session_state:
        st.session_state.current_chat_file = None

    left, right = st.columns([8, 2])

    # with left:
    #     if st.button("➕ New Chat"):
    #         st.session_state.messages = []
    #         st.session_state.current_chat_file = None
    #         st.rerun()

    # ---------- VOICE INPUT ----------
    with right:

        components.html(
        """
        <button id="voice-btn">🎤</button>

        <script>

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        recognition.lang = "en-US";
        recognition.interimResults = false;

        let recording = false;

        const btn = document.getElementById("voice-btn");

        btn.onclick = () => {

            if(!recording){
                recognition.start();
                recording = true;
                btn.innerText = "⏹";
            }
            else{
                recognition.stop();
                recording = false;
                btn.innerText = "🎤";
            }
        };

        recognition.onresult = function(event){

            const text = event.results[0][0].transcript;

            const textarea = window.parent.document.querySelector("textarea");

            if(textarea){

                textarea.value = text;

                textarea.dispatchEvent(new Event("input",{bubbles:true}));

                const enterEvent = new KeyboardEvent("keydown", {
                    bubbles: true,
                    cancelable: true,
                    key: "Enter",
                    code: "Enter"
                });

                textarea.dispatchEvent(enterEvent);
            }
        };

        recognition.onend = function(){
            recording = false;
            btn.innerText = "🎤";
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
            background:white;
            color:black;
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
        height=40
        )


    # ---------- HEADER ----------
#     st.title("🤖 VizTalk")


#     st.markdown("""
# Ask business questions in natural language and instantly generate dashboards.

# Example queries:



    # ---------- DISPLAY CHAT ----------
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.write(msg["content"])

            if "data" in msg:

                df = pd.DataFrame(msg["data"])

                if not df.empty:

                    st.dataframe(df)

                    chart = msg.get("chart")
                    x = msg.get("x")
                    y = msg.get("y")

                    if x in df.columns and y in df.columns:

                        if chart == "bar":
                            st.bar_chart(df.set_index(x)[y])

                        elif chart == "line":
                            st.line_chart(df.set_index(x)[y])

                else:
                    st.warning("No data returned from this query.")

    prompt = st.chat_input("Ask a question about your data")

    if prompt:

        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        save_chat()

        loading_phrases = [
            "Analyzing your data.",
            "Let me check the dataset.",
            "Generating your dashboard."
        ]

        auto_speak(random.choice(loading_phrases))

        with st.spinner("Generating dashboard..."):

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

                if df.empty:

                    message = "I couldn't find data for that query. Please try a different question."

                    st.warning(message)

                    auto_speak(message)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": message
                    })

                    save_chat()
                    return

            except Exception:

                message = "I couldn't understand that query. Try asking about revenue, region, product, or month."

                st.error(message)

                auto_speak(message)

                return

        with st.chat_message("assistant"):

            with st.expander("View generated SQL"):
                st.code(sql)

            st.write("Query Result")
            st.dataframe(df)

            if x not in df.columns or y not in df.columns:

                message = "The requested data fields do not exist in this dataset."

                st.error(message)

                auto_speak(message)

                return

            if x in df.columns and y in df.columns:

                if chart == "bar":
                    st.bar_chart(df.set_index(x)[y])

                elif chart == "line":
                    st.line_chart(df.set_index(x)[y])

            insights = generate_insight(df, x, y)

            st.subheader("Key Insights")

            for insight in insights:
                st.write("•", insight)

            auto_speak(insights[0])

        st.session_state.messages.append({
            "role": "assistant",
            "content": insights[0],
            "data": data,
            "chart": chart,
            "x": x,
            "y": y
        })

        save_chat()