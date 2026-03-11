import streamlit as st
import streamlit.components.v1 as components
import os
import json
import requests
import pandas as pd
import random
from streamlit_mic_recorder import mic_recorder
import whisper

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"

CHAT_DIR = "saved_chats"
API_URL = "http://127.0.0.1:8000/query"


# ---------- FORCE TEXT TO BLACK ----------
st.markdown("""
<style>

/* Entire app text */
.stApp {
    color: black !important;
    background-color: white;
}

/* Markdown text */
.stMarkdownContainer,
.stMarkdownContainer p,
.stMarkdownContainer span {
    color: black !important;
}

/* Headers like Hello Anisha */
.stMarkdownContainer h1,
.stMarkdownContainer h2,
.stMarkdownContainer h3,
.stMarkdownContainer h4 {
    color: black !important;
}

/* Chat messages */
.stChatMessage * {
    color: black !important;
}

/* Chat input */
textarea {
    color: black !important;
}

/* Dataframe */
[data-testid="stDataFrame"] * {
    color: black !important;
}

/* Chart labels */
svg text {
    fill: black !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- LOAD WHISPER ----------
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()


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


# ---------- RUN QUERY ----------
def run_query(prompt, from_voice=False):

    st.session_state.messages.append({
        "role": "user",
        "content": str(prompt)
    })

    save_chat()

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

        except Exception as e:
            st.error(f"Backend error: {e}")
            return

    st.session_state.messages.append({
        "role": "assistant",
        "content": "Here is the generated dashboard",
        "sql": sql,
        "data": data,
        "chart": chart,
        "x": x,
        "y": y
    })


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


    # ---------- VOICE INPUT ----------
    with right:

        audio = mic_recorder(
            start_prompt="🎤 Speak",
            stop_prompt="⏹ Stop",
            just_once=True,
            use_container_width=True,
            key="voice_recorder"
        )

        if audio is not None:

            audio_bytes = audio["bytes"]

            temp_audio_path = "temp_audio.wav"

            with open(temp_audio_path, "wb") as f:
                f.write(audio_bytes)

            if os.path.exists(temp_audio_path):

                result = model.transcribe(
                    temp_audio_path,
                    fp16=False,
                    language="en"
                )

                text = result["text"].strip()

                if text:
                    st.info(f"🎤 You said: {text}")
                    run_query(text, from_voice=True)

                os.remove(temp_audio_path)


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

                        elif chart == "pie":

                            pie_data = df.set_index(x)[y]

                            fig = pie_data.plot.pie(
                                autopct="%1.1f%%",
                                ylabel="",
                                figsize=(5,5)
                            ).figure

                            st.pyplot(fig)

                        elif chart == "hbar":

                            st.write("Horizontal Bar Chart")
                            st.bar_chart(df.set_index(x)[y].sort_values())

                        elif chart == "area":

                            st.area_chart(df.set_index(x)[y])

                        elif chart == "scatter":

                            scatter_df = df[[x, y]]
                            st.scatter_chart(scatter_df)

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

                elif chart == "pie":

                    pie_data = df.set_index(x)[y]

                    fig = pie_data.plot.pie(
                        autopct="%1.1f%%",
                        ylabel="",
                        figsize=(5,5)
                    ).figure

                    st.pyplot(fig)

                elif chart == "hbar":

                    st.write("Horizontal Bar Chart")
                    st.bar_chart(df.set_index(x)[y].sort_values())

                elif chart == "area":

                    st.area_chart(df.set_index(x)[y])

                elif chart == "scatter":

                    scatter_df = df[[x, y]]
                    st.scatter_chart(scatter_df)

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