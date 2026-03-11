# # import streamlit as st
# # import json
# # import os
# # from frontend.landing_ui import render_landing
# # from frontend.chat_ui import render_chat
# # from frontend.sidebar import render_sidebar
# # from streamlit_cookies_manager import EncryptedCookieManager

# # cookies = EncryptedCookieManager(
# #     prefix="viztalk_",
# #     password="my_secret_password"
# # )

# # if not cookies.ready():
# #     st.stop()

# # st.set_page_config(
# #     page_title="VizTalk",
# #     page_icon="favicon.png",
# #     layout="wide"
# # )

# # st.markdown("""
# # <style>

# # /* App background */
# # [data-testid="stAppViewContainer"]{
# #     background-color:white;
# # }

# # /* Main content */
# # [data-testid="stAppViewBlockContainer"]{
# #     background-color:white;
# #     color:black;
# # }

# # /* Sidebar */
# # [data-testid="stSidebar"]{
# #     background-color:#0F2D52 !important;
# # }
# # /* Sidebar text */
# # [data-testid="stSidebar"] *{
# #     color:white !important;
# # }
# # /* Sidebar buttons */
# # [data-testid="stSidebar"] .stButton>button{
# #     background-color:#FFD700 !important;
# #     color:black !important;
# # }

# # /* Header */
# # header[data-testid="stHeader"]{
# #     background-color:white;
# # }

# # /* All text */
# # h1, h2, h3, h4, h5, h6, p, span, label, div{
# #     color:black !important;
# # }

# # /* -------- INPUT FIELDS -------- */

# # /* Streamlit text input container */
# # [data-baseweb="input"]{
# #     background-color:white !important;
# # }

# # /* Actual input field */
# # [data-baseweb="input"] input{
# #     background-color:white !important;
# #     color:black !important;
# # }

# # /* Placeholder */
# # [data-baseweb="input"] input::placeholder{
# #     color:#777 !important;
# # }

# # /* File uploader */
# # [data-testid="stFileUploader"]{
# #     background-color:white !important;
# #     color:black !important;
# # }

# # /* Chat input */
# # [data-testid="stChatInput"]{
# #     background-color:white !important;
# #     color:black !important;
# # }

# # /* Bottom chat bar */
# # [data-testid="stBottomBlockContainer"]{
# #     background-color:white !important;
# # }

# # /* Buttons */
# # .stButton>button{
# #     background-color:#4CAF50;
# #     color:white;
# #     border-radius:8px;
# # }

# # /* Sidebar file uploader container */
# # [data-testid="stSidebar"] [data-testid="stFileUploader"]{
# #     background-color:white !important;
# #     color:black !important;
# # }

# # /* Upload drop area */
# # [data-testid="stFileUploaderDropzone"]{
# #     background-color:white !important;
# #     color:black !important;
# #     border:1px solid #ccc !important;
# # }

# # /* BaseWeb uploader element */
# # [data-baseweb="file-uploader"]{
# #     background-color:white !important;
# #     color:black !important;
# # }

# # /* Text inside uploader */
# # [data-baseweb="file-uploader"] span{
# #     color:black !important;
# # }

# # /* Upload button */
# # /* Sidebar upload button */
# # [data-testid="stSidebar"] [data-testid="stFileUploader"] button{
# #     background-color:#FFD700 !important;
# #     color:black !important;

# # }
            
# # /* Code blocks (st.code) */
# # pre {
# #     background-color: white !important;
# #     color: black !important;
# #     border: 1px solid #e6e6e6 !important;
# # }

# # /* Code text */
# # code {
# #     background-color: white !important;
# #     color: black !important;
# # }

# # /* Streamlit code container */
# # [data-testid="stCodeBlock"] {
# #     background-color: white !important;
# # }

# # /* SQL syntax text */
# # [data-testid="stCodeBlock"] span {
# #     color: black !important;
# # }

# # </style>
# # """, unsafe_allow_html=True)


# # # -------- SESSION STATE --------
# # if "page" not in st.session_state:
# #     st.session_state.page = "landing"

# # # Load user from cookie
# # if "user" not in st.session_state:
# #     st.session_state.user = cookies.get("user")


# # # -------- USER STORAGE --------
# # USER_FILE = "users.json"

# # if not os.path.exists(USER_FILE):
# #     with open(USER_FILE, "w") as f:
# #         json.dump({}, f)


# # def load_users():
# #     with open(USER_FILE) as f:
# #         return json.load(f)


# # def save_users(users):
# #     with open(USER_FILE, "w") as f:
# #         json.dump(users, f)


# # # -------- LANDING PAGE --------
# # if st.session_state.page == "landing":
# #     render_landing()


# # # -------- LOGIN PAGE --------
# # elif st.session_state.page == "login":

# #     if st.session_state.get("login_alert"):
# #         st.warning("⚠️ Please login before you continue.")
# #         st.session_state.login_alert = False

# #     st.title("Login / Register")

# #     username = st.text_input("Username")
# #     password = st.text_input("Password", type="password")

# #     col1, col2 = st.columns(2)

# #     # LOGIN
# #     with col1:
# #         if st.button("Login"):
# #             users = load_users()

# #             if username in users and users[username] == password:

# #                 st.session_state.user = username

# #                 # -------- COOKIE SAVE --------
# #                 cookies["user"] = username
# #                 cookies.save()

# #                 st.session_state.page = "chat"
# #                 st.success("Login successful")
# #                 st.rerun()

# #             else:
# #                 st.error("Invalid credentials")

# #     # REGISTER
# #     with col2:
# #         if st.button("Register"):
# #             users = load_users()

# #             if username in users:
# #                 st.warning("User already exists")
# #             else:
# #                 users[username] = password
# #                 save_users(users)
# #                 st.success("Account created! Please login.")


# # # -------- CHAT PAGE --------
# # elif st.session_state.page == "chat":

# #     if not st.session_state.user:
# #         st.session_state.login_alert = True
# #         st.session_state.page = "login"
# #         st.rerun()

# #     # Sidebar visible only in chat
# #     render_sidebar()

# #     # Main chat UI
# #     render_chat()


# import streamlit as st
# import json
# import os
# from frontend.landing_ui import render_landing
# from frontend.chat_ui import render_chat
# from frontend.sidebar import render_sidebar
# from streamlit_cookies_manager import EncryptedCookieManager

# cookies = EncryptedCookieManager(
#     prefix="viztalk_",
#     password="my_secret_password"
# )

# if not cookies.ready():
#     st.stop()

# st.set_page_config(
#     page_title="VizTalk",
#     page_icon="favicon.png",
#     layout="wide"
# )

# st.markdown("""
# <style>

# /* App background */
# [data-testid="stAppViewContainer"]{
#     background-color:white;
# }

# /* Main content */
# [data-testid="stAppViewBlockContainer"]{
#     background-color:white;
#     color:black;
# }

# # /* -------- SIDEBAR STYLING -------- */

# # /* Sidebar background */
# # [data-testid="stSidebar"]{
# #     background-color:#102A43 !important;
# # }

# # /* Sidebar text */
# # [data-testid="stSidebar"] *{
# #     color:#F1F5F9 !important;
# # }

# # /* Sidebar divider */
# # [data-testid="stSidebar"] hr{
# #     border-color:#2C4A66 !important;
# # }

# # /* Sidebar buttons */
# # [data-testid="stSidebar"] .stButton>button{
# #     background-color:#FACC15 !important;
# #     color:#1E293B !important;
# #     border-radius:8px;
# #     font-weight:600;
# # }

# # /* Sidebar button hover */
# # [data-testid="stSidebar"] .stButton>button:hover{
# #     background-color:#EAB308 !important;
# # }


# /* -------- SIDEBAR STYLING -------- */

# section[data-testid="stSidebar"]{
#     background-color:#1B263B !important;   /* deep navy */
# }

# /* force sidebar text to white */
# section[data-testid="stSidebar"] h1,
# section[data-testid="stSidebar"] h2,
# section[data-testid="stSidebar"] h3,
# section[data-testid="stSidebar"] h4,
# section[data-testid="stSidebar"] p,
# section[data-testid="stSidebar"] span,
# section[data-testid="stSidebar"] div{
#     color:#F8FAFC !important;
# }

# /* sidebar divider */
# section[data-testid="stSidebar"] hr{
#     border-color:#3A506B !important;
# }

# /* sidebar buttons */
# section[data-testid="stSidebar"] .stButton>button{
#     background-color:#FBBF24 !important;
#     color:#111827 !important;
#     border-radius:8px;
#     font-weight:600;
# }

# /* button hover */
# section[data-testid="stSidebar"] .stButton>button:hover{
#     background-color:#F59E0B !important;
# }            


# /* Header */
# header[data-testid="stHeader"]{
#     background-color:white;
# }

# /* All text */
# h1, h2, h3, h4, h5, h6, p, span, label, div{
#     color:black !important;
# }

# /* -------- INPUT FIELDS -------- */

# [data-baseweb="input"]{
#     background-color:white !important;
# }

# [data-baseweb="input"] input{
#     background-color:white !important;
#     color:black !important;
# }

# [data-baseweb="input"] input::placeholder{
#     color:#777 !important;
# }

# /* File uploader */
# [data-testid="stFileUploader"]{
#     background-color:white !important;
#     color:black !important;
# }

# /* Chat input */
# [data-testid="stChatInput"]{
#     background-color:white !important;
#     color:black !important;
# }

# /* Bottom chat bar */
# [data-testid="stBottomBlockContainer"]{
#     background-color:white !important;
# }

# /* Buttons (main UI) */
# .stButton>button{
#     background-color:#4CAF50;
#     color:white;
#     border-radius:8px;
# }

# /* Sidebar file uploader container */
# [data-testid="stSidebar"] [data-testid="stFileUploader"]{
#     background-color:#1B3B5F !important;
#     color:white !important;
# }

# /* Upload drop area */
# [data-testid="stFileUploaderDropzone"]{
#     background-color:white !important;
#     color:black !important;
#     border:1px solid #ccc !important;
# }

# /* BaseWeb uploader element */
# [data-baseweb="file-uploader"]{
#     background-color:white !important;
#     color:black !important;
# }

# /* Text inside uploader */
# [data-baseweb="file-uploader"] span{
#     color:black !important;
# }

# /* Sidebar upload button */
# [data-testid="stSidebar"] [data-testid="stFileUploader"] button{
#     background-color:#FACC15 !important;
#     color:#1E293B !important;
# }
            
# /* Code blocks (st.code) */
# pre {
#     background-color: white !important;
#     color: black !important;
#     border: 1px solid #e6e6e6 !important;
# }

# /* Code text */
# code {
#     background-color: white !important;
#     color: black !important;
# }

# /* Streamlit code container */
# [data-testid="stCodeBlock"] {
#     background-color: white !important;
# }

# /* SQL syntax text */
# [data-testid="stCodeBlock"] span {
#     color: black !important;
# }

# </style>
# """, unsafe_allow_html=True)


# # -------- SESSION STATE --------
# if "page" not in st.session_state:
#     st.session_state.page = "landing"

# # Load user from cookie
# if "user" not in st.session_state:
#     st.session_state.user = cookies.get("user")


# # -------- USER STORAGE --------
# USER_FILE = "users.json"

# if not os.path.exists(USER_FILE):
#     with open(USER_FILE, "w") as f:
#         json.dump({}, f)


# def load_users():
#     with open(USER_FILE) as f:
#         return json.load(f)


# def save_users(users):
#     with open(USER_FILE, "w") as f:
#         json.dump(users, f)


# # -------- LANDING PAGE --------
# if st.session_state.page == "landing":
#     render_landing()

    
# # -------- LOGIN PAGE --------
# elif st.session_state.page == "login":

#     if st.session_state.get("login_alert"):
#         st.warning("⚠️ Please login before you continue.")
#         st.session_state.login_alert = False

#     st.title("Login / Register")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     col1, col2 = st.columns(2)

#     # LOGIN
#     with col1:
#         if st.button("Login"):
#             users = load_users()

#             if username in users and users[username] == password:

#                 st.session_state.user = username

#                 cookies["user"] = username
#                 cookies.save()

#                 st.session_state.page = "chat"
#                 st.success("Login successful")
#                 st.rerun()

#             else:
#                 st.error("Invalid credentials")

#     # REGISTER
#     with col2:
#         if st.button("Register"):
#             users = load_users()

#             if username in users:
#                 st.warning("User already exists")
#             else:
#                 users[username] = password
#                 save_users(users)
#                 st.success("Account created! Please login.")


# # -------- CHAT PAGE --------
# elif st.session_state.page == "chat":

#     if not st.session_state.user:
#         st.session_state.login_alert = True
#         st.session_state.page = "login"
#         st.rerun()

#     render_sidebar()
#     render_chat()

import streamlit as st
import json
import os
from frontend.landing_ui import render_landing
from frontend.chat_ui import render_chat
from frontend.sidebar import render_sidebar
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="viztalk_",
    password="my_secret_password"
)

if not cookies.ready():
    st.stop()

st.set_page_config(
    page_title="VizTalk",
    page_icon="favicon.png",
    layout="wide"
)

# -------- GLOBAL STYLING --------
st.markdown("""
<style>

/* MAIN APP BACKGROUND */
[data-testid="stAppViewContainer"]{
    background-color:#0E1117;
}

/* MAIN CONTENT AREA */
[data-testid="stAppViewBlockContainer"]{
    background-color:#0E1117;
    color:white;
}

/* Header */
header[data-testid="stHeader"]{
    background-color:#0E1117;
}

/* Chat input bar */
[data-testid="stChatInput"]{
    background-color:#0E1117 !important;
    color:white !important;
}

/* Inputs */
[data-baseweb="input"] input{
    background-color:#1E1E1E !important;
    color:white !important;
}

/* Buttons */
.stButton>button{
    background-color:#2563EB;
    color:white;
}

</style>
""", unsafe_allow_html=True)
# -------- SESSION STATE --------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "user" not in st.session_state:
    st.session_state.user = cookies.get("user")


# -------- USER STORAGE --------
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE) as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


# -------- LANDING PAGE --------
if st.session_state.page == "landing":
    render_landing()

    # Animated background
    st.markdown("""
    <style>

    [data-testid="stAppViewContainer"]{
        background: linear-gradient(
            -45deg,
            #cfe8ff,
            #e0d4ff,
            #ffe0cc,
            #d7f5e0,
            #ffd9e6
        );
        background-size: 400% 400%;
        animation: gradientMove 12s ease infinite;
    }

    [data-testid="stAppViewBlockContainer"]{
        background: transparent !important;
    }

    @keyframes gradientMove{
        0%{background-position:0% 50%;}
        50%{background-position:100% 50%;}
        100%{background-position:0% 50%;}
    }

    </style>
    """, unsafe_allow_html=True)


# -------- LOGIN PAGE --------
elif st.session_state.page == "login":

    # Animated background for login page
    st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        -45deg,
        #cfe8ff,
        #e0d4ff,
        #ffe0cc,
        #d7f5e0,
        #ffd9e6
    );
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
}

[data-testid="stAppViewBlockContainer"]{
    background: transparent !important;
}

/* ---- MAKE LOGIN TEXT BLACK ---- */

h1, h2, h3, h4, h5, h6{
    color:black !important;
}

label{
    color:black !important;
}

p{
    color:black !important;
}

div[data-testid="stMarkdownContainer"]{
    color:black !important;
}

@keyframes gradientMove{
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}

</style>
""", unsafe_allow_html=True)

    if st.session_state.get("login_alert"):
        st.warning("⚠️ Please login before you continue.")
        st.session_state.login_alert = False

    st.title("Login / Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    st.write("")

    # LOGIN
    st.markdown("### Existing Account?")

    if st.button("Login"):
        users = load_users()

        if username in users and users[username] == password:

            st.session_state.user = username

            cookies["user"] = username
            cookies.save()

            st.session_state.page = "chat"
            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid credentials")

    st.write("")

    # REGISTER
    st.markdown("### Don't have an account?")

    if st.button("Register"):
        users = load_users()

        if username in users:
            st.warning("User already exists")
        else:
            users[username] = password
            save_users(users)
            st.success("Account created! Please login.")


# -------- CHAT PAGE --------
elif st.session_state.page == "chat":

    if not st.session_state.user:
        st.session_state.login_alert = True
        st.session_state.page = "login"
        st.rerun()

    render_sidebar()
    render_chat()