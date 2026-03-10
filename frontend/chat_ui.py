# import streamlit as st
# import streamlit.components.v1 as components
# import os
# import json

# CHAT_DIR = "saved_chats"


# def save_current_chat():
#     if not os.path.exists(CHAT_DIR):
#         os.makedirs(CHAT_DIR)

#     files = os.listdir(CHAT_DIR)
#     chat_id = len(files)

#     filename = f"{CHAT_DIR}/chat_{chat_id}.json"

#     with open(filename, "w") as f:
#         json.dump(st.session_state.messages, f)


# def render_chat():

#     # ---------- SESSION STATE ----------
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # ---------- TOP CONTROLS ----------
#     left, right = st.columns([8,2])

#     with left:
#         if st.button("➕ New Chat"):

#             if len(st.session_state.messages) > 0:
#                 save_current_chat()

#             st.session_state.messages = []
#             st.rerun()

    
#     with right:
#         st.write("")
#         components.html(
#             """
#             <div id="voice-container">
#                 <button id="voice-btn">🎤</button>
#                 <span id="voice-status"></span>
#             </div>

#             <script>
#             const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
#             const recognition = new SpeechRecognition();

#             recognition.lang = "en-US";
#             recognition.interimResults = false;
#             recognition.maxAlternatives = 1;

#             const btn = document.getElementById("voice-btn");
#             const status = document.getElementById("voice-status");

#             btn.onclick = () => {
#                 recognition.start();
#                 status.innerText = "Listening...";
#             };

#             recognition.onresult = function(event){
#                 const text = event.results[0][0].transcript;
#                 status.innerText = "";

#                 const textarea = window.parent.document.querySelector("textarea");

#                 if(textarea){
#                     textarea.value = text;

#                     textarea.dispatchEvent(
#                         new Event("input", { bubbles: true })
#                     );
#                 }
#             };

#             recognition.onerror = function(){
#                 status.innerText = "Mic error";
#             };

#             recognition.onend = function(){
#                 status.innerText = "";
#             };
#             </script>

#             <style>
#             #voice-container{
#                 position: fixed;
#                 bottom: 22px;
#                 right: 120px;
#                 display:flex;
#                 align-items:center;
#                 gap:8px;
#                 z-index:9999;
#             }

#             #voice-btn{
#                 font-size:18px;
#                 padding:6px 10px;
#                 border-radius:8px;
#                 border:none;
#                 background:#262730;
#                 color:white;
#                 cursor:pointer;
#             }

#             #voice-btn:hover{
#                 background:#3a3b47;
#             }

#             #voice-status{
#                 color:#aaa;
#                 font-size:12px;
#             }
#             </style>
#             """,
#             height=80
#         )

#     st.divider()

#     # ---------- DISPLAY CHAT ----------
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     # ---------- CHAT INPUT ----------
#     prompt = st.chat_input("Ask a question about your data")

#     if prompt:

#         with st.chat_message("user"):
#             st.write(prompt)

#         st.session_state.messages.append({
#             "role": "user",
#             "content": prompt
#         })

#         # Temporary response placeholder
#         response = "Processing your request..."

#         with st.chat_message("assistant"):
#             st.write(response)

#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": response
#         })


import streamlit as st
import streamlit.components.v1 as components
import os
import json

CHAT_DIR = "saved_chats"


def save_current_chat():

    if not os.path.exists(CHAT_DIR):
        os.makedirs(CHAT_DIR)

    if len(st.session_state.messages) == 0:
        return

    # find first user message
    first_msg = None
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            first_msg = msg["content"]
            break

    if first_msg:
        words = first_msg.split()[:3]  # first 3 words
        title = "_".join(words).lower()
    else:
        title = "chat"

    filename = f"{CHAT_DIR}/{title}.json"

    with open(filename, "w") as f:
        json.dump(st.session_state.messages, f)


def render_chat():

    # ---------- SESSION STATE ----------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ---------- TOP CONTROLS ----------
    left, right = st.columns([8,2])

    with left:
        if st.button("➕ New Chat"):

            if len(st.session_state.messages) > 0:
                save_current_chat()

            st.session_state.messages = []
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
                    btn.innerHTML = "⏹";   // show stop icon
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
                btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="white">
                <path d="M12 15a3 3 0 003-3V5a3 3 0 10-6 0v7a3 3 0 003 3zm5-3a1 1 0 10-2 0 3 3 0 11-6 0 1 1 0 10-2 0 5 5 0 004 4.9V21H9a1 1 0 100 2h6a1 1 0 100-2h-2v-2.1A5 5 0 0017 12z"/>
                </svg>`;
                status.innerText = "";
            };

            recognition.onerror = function(){
                isRecording = false;
                btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="white">
                <path d="M12 15a3 3 0 003-3V5a3 3 0 10-6 0v7a3 3 0 003 3zm5-3a1 1 0 10-2 0 3 3 0 11-6 0 1 1 0 10-2 0 5 5 0 004 4.9V21H9a1 1 0 100 2h6a1 1 0 100-2h-2v-2.1A5 5 0 0017 12z"/>
                </svg>`;
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

    # st.divider()

    # ---------- DISPLAY CHAT ----------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ---------- CHAT INPUT ----------
    prompt = st.chat_input("Ask a question about your data")

    if prompt:

        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        response = "Processing your request..."

        with st.chat_message("assistant"):
            st.write(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })