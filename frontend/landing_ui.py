
import streamlit as st

def render_landing():
    st.markdown("""
<style>
/* Apply animated gradient directly to Streamlit app container */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        -45deg,
        #cfe8ff,
        #e0d4ff,
        #d7f5e0,
        #ffd9e6
    );
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
}
h1, h2, h3, h4, h5, h6,
p, span, div, label, li, b {
    color: black !important;
}

/* Keep inner container transparent */
[data-testid="stAppViewBlockContainer"]{
    background: transparent !important;
}

/* Smooth gradient animation */
@keyframes gradientMove{
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}

</style>



""", unsafe_allow_html=True)

    # ---------- HERO SECTION ----------
    col1, col2 = st.columns([8,1])

    with col2:
        if st.button("Login / Register"):
            st.session_state.page = "login"
            st.rerun()

    # st.markdown(
    #     """
    #     <h1 style='text-align:center;'>VizTalk!</h1>
    #     """,
    #     unsafe_allow_html=True
    # )
    import streamlit.components.v1 as components

    components.html("""
    <h1 id="viztalk-title" style="
    text-align:center;
    font-size:52px;
    font-weight:800;
    margin:20px;
    background: linear-gradient(90deg,#000000,#000000,#000000,#000000);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-family:sans-serif;
    "></h1>

    <script>
    const text = "VizTalk";
    const speed = 150;

    let i = 0;

    function typeWriter() {
        if (i < text.length) {
            document.getElementById("viztalk-title").innerHTML += text.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
    }

    typeWriter();
    </script>
    """, height=80)

    # st.markdown(
    #     """
    #     <p style='text-align:center; font-size:18px;'>
    #     Ask questions and instantly get insights and visualizations about your data.
    #     </p>
    #     """,
    #     unsafe_allow_html=True
    # )
    st.markdown("""
<div style="overflow:hidden; white-space:nowrap;">
<div style="
display:inline-block;
padding-left:100%;
animation: scroll 18s linear infinite;
font-size:18px;
color:#1B263B;
font-weight:500;">
Ask questions and instantly get insights and visualizations about your data • Explore datasets using natural language • Generate dashboards instantly
</div>
</div>

<style>
@keyframes scroll {
0% { transform: translateX(0); }
100% { transform: translateX(-100%); }
}
</style>
""", unsafe_allow_html=True)

    # st.markdown(
    #     """
    #     <p style='text-align:center; font-size:16px; color:gray;'>
    #     This platform allows users to explore datasets using natural language.
    #     Simply type your question and the system automatically generates charts,
    #     metrics, and dashboards to help you understand your data quickly.
    #     </p>
    #     """,
    #     unsafe_allow_html=True
    # )
    st.markdown("""
<div style="
background:#F8FAFC;
padding:25px;
border-radius:12px;
border:1px solid #E2E8F0;
text-align:center;
max-width:900px;
margin:auto;
color:#1B263B;
background-color: white;
font-size:10px;
font-size:17px;
line-height:1.6;
">

 <b>Transform raw data into insights using natural language.</b><br><br>

This platform allows users to explore datasets without writing SQL or building dashboards manually.  
Simply ask a question and the system automatically generates charts and visual dashboards to help you understand your data instantly.

</div>
""", unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([3,1,3])

    # with col2:
    #     if st.button("Get Started 🚀"):
    #         st.session_state.page = "chat"
    #         st.rerun()

    st.write("")
    st.write("")
    st.divider()

  


    # st.subheader("Key Features")

    # col1, col2 = st.columns(2)

    # with col1:
    #     st.markdown("""
    # <div style="
    # border:1px solid #e6e6e6;
    # padding:20px;
    # border-radius:10px;
    # margin-bottom:15px;
    # background-color:#f9f9f9;
    # color:black;">    
    # <h4>💬 Natural Language Queries</h4>
    # <p>Ask questions about your data in plain English without writing SQL.</p>
    # </div>
    # """, unsafe_allow_html=True)

    #     st.markdown("""
    #     <div style="
    #     border:1px solid #e6e6e6;
    #     padding:20px;
    #     border-radius:10px;
    #     background-color:#f9f9f9;
    #     color:black;">
    #     <h4>📊 Automatic Dashboard Generation</h4>
    #     <p>Charts and insights are automatically created based on your query.</p>
    #     </div>
    #     """, unsafe_allow_html=True)

    # with col2:
    #     st.markdown("""
    #     <div style="
    #     border:1px solid #e6e6e6;
    #     padding:20px;
    #     border-radius:10px;
    #     margin-bottom:15px;
    #     background-color:#f9f9f9;
    #     color:black;">
    #     <h4>🎤 Voice Queries</h4>
    #     <p>Ask questions using voice commands.</p>
    #     </div>
    #     """, unsafe_allow_html=True)

    #     st.markdown("""
    #     <div style="
    #     border:1px solid #e6e6e6;
    #     padding:10px;
    #     border-radius:10px;
    #     background-color:#f9f9f9;
    #     color:black;">
    #     <h4>📁 Dataset Upload</h4>
    #     <p>Upload your own dataset and instantly explore insights.</p>
    #     </div>
    #     """, unsafe_allow_html=True)
    # st.write("")
    # st.divider()


    st.subheader("Key Features")

    st.markdown("""
    <style>

    .flip-container{
        display:flex;
        justify-content:center;
        gap:25px;
        flex-wrap:wrap;
        margin-top:20px;
    }

    .flip-card{
        background:transparent;
        width:220px;
        height:150px;
        perspective:1000px;
    }
    .flip-card-inner{
        position:relative;
        width:100%;
        height:100%;
        transition:transform 0.6s;
        transform-style:preserve-3d;
    }
    

    .flip-card:hover .flip-card-inner{
        transform:rotateY(180deg);
    }

    .flip-card-front, .flip-card-back{
        position:absolute;
        width:100%;
        height:100%;
        backface-visibility:hidden;
        border-radius:10px;
        display:flex;
        align-items:center;
        justify-content:center;
        text-align:center;
        padding:15px;
        box-shadow:0 4px 10px rgba(0,0,0,0.1);
    }

    .flip-card-front{
        background:white;
        font-weight:600;
        font-size:16px;
    }

    .flip-card-back{
        background:#0F2D52;
        color:white;
        transform:rotateY(180deg);
        font-size:14px;
    }
   /* CARD 1 */
    .flip-card:nth-child(1) .flip-card-front{
         background:#C7D2FE;
         color:#1E293B;
    }

    .flip-card:nth-child(1) .flip-card-back{
        background:#C7D2FE;
        color:#1E293B;
    }

    /* CARD 2 */
    .flip-card:nth-child(2) .flip-card-front{
        background:#BBF7D0;
        color:#065F46;
    }

    .flip-card:nth-child(2) .flip-card-back{
        background:#BBF7D0;
        color:#065F46;
    }

    /* CARD 3 */
    .flip-card:nth-child(3) .flip-card-front{
        background:#FED7AA;
        color:#9A3412;
    }

    .flip-card:nth-child(3) .flip-card-back{
        background:#FED7AA;
        color:#9A3412;
    }

    /* CARD 4 */
    .flip-card:nth-child(4) .flip-card-front{
        background:#BAE6FD;
        color:#075985;
    }

    .flip-card:nth-child(4) .flip-card-back{
        background:#BAE6FD;
        color:#075985;
    }

    </style>

    <div class="flip-container">

    <div class="flip-card">
    <div class="flip-card-inner">
    <div class="flip-card-front">💬 Natural Language Queries</div>
    <div class="flip-card-back">
    Ask questions about your data in plain English without writing SQL.
    </div>
    </div>
    </div>

    <div class="flip-card">
    <div class="flip-card-inner">
    <div class="flip-card-front">📊 Automatic Dashboards</div>
    <div class="flip-card-back">
    Charts and insights are automatically generated from your questions.
    </div>
    </div>
    </div>

    <div class="flip-card">
    <div class="flip-card-inner">
    <div class="flip-card-front">🎤 Voice Queries</div>
    <div class="flip-card-back">
    Ask questions using voice commands instead of typing.
    </div>
    </div>
    </div>

    <div class="flip-card">
    <div class="flip-card-inner">
    <div class="flip-card-front">📁 Dataset Upload</div>
    <div class="flip-card-back">
    Upload CSV datasets and instantly explore insights and dashboards.
    </div>
    </div>
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    # ---------- HOW IT WORKS ----------

    st.subheader("How It Works")

    st.markdown("""
    <style>

    .pipeline-wrapper{
    display:flex;
    justify-content:center;
    align-items:center;
    gap:20px;
    flex-wrap:wrap;
    margin-top:40px;
    }

    .pipeline-box{
    background:#BAE6FD;   /* light blue */
    color:#075985;        /* dark blue text */
    padding:14px 20px;
    border-radius:10px;
    font-size:14px;
    font-weight:600;
    box-shadow:0 6px 16px rgba(0,0,0,0.12);
    min-width:140px;
    text-align:center;
    }

    .pipeline-arrow{
    font-size:26px;
    color:#0369A1;
    font-weight:bold;
    }

    </style>

    <div class="pipeline-wrapper">

    <div class="pipeline-box">User Login</div>
    <div class="pipeline-arrow">→</div>

    <div class="pipeline-box">Upload Dataset</div>
    <div class="pipeline-arrow">→</div>

    <div class="pipeline-box">Text / Voice Query</div>
    <div class="pipeline-arrow">→</div>

    <div class="pipeline-box">LLM Processing</div>
    <div class="pipeline-arrow">→</div>

    <div class="pipeline-box">SQL Query Generation</div>
    <div class="pipeline-arrow">→</div>

    <div class="pipeline-box">Data Retrieval</div>
    <div class="pipeline-arrow">→</div>

    <div class="pipeline-box">Chart Generation</div>
    <div class="pipeline-arrow">→</div>

    <div class="pipeline-box">Interactive Dashboard</div>
    <div class="pipeline-arrow">→</div>

    <div class="pipeline-box">Chat History Saved</div>

    </div>
    """, unsafe_allow_html=True)
    # col1, col2, col3 = st.columns([1,2,1])

    # with col2:
    #     st.image("frontend/images/how-it-works-img.png", width=700)

    st.write("")
    st.divider()

    # ---------- EXAMPLE QUERIES ----------
    
    st.markdown("""
<style>

.query-wrapper{
    overflow:hidden;
    white-space:nowrap;
    margin-top:20px;
}

.query-track{
    display:inline-flex;
    gap:20px;
    animation:scrollQueries 18s linear infinite;
}

.query-card{
    background:#F8FAFC;
    border:1px solid #E2E8F0;
    border-radius:10px;
    padding:12px 18px;
    font-size:14px;
    color:#1B263B;
    min-width:230px;
    text-align:center;
    box-shadow:0 3px 8px rgba(0,0,0,0.08);
}

.query-card:hover{
    transform:scale(1.05);
    transition:0.2s;
}

@keyframes scrollQueries{
    0%{transform:translateX(0);}
    100%{transform:translateX(-50%);}
}

</style>

<div style="text-align:center; font-weight:600; margin-bottom:10px;">
 Try asking
</div>

<div class="query-wrapper">
<div class="query-track">

<div class="query-card">Show revenue by campaign type</div>
<div class="query-card">Show monthly revenue trends</div>
<div class="query-card">Compare marketing channel performance</div>
<div class="query-card">Show top performing products</div>

<!-- duplicated for smooth scrolling -->
<div class="query-card">Show revenue by campaign type</div>
<div class="query-card">Show monthly revenue trends</div>
<div class="query-card">Compare marketing channel performance</div>
<div class="query-card">Show top performing products</div>

</div>
</div>
""", unsafe_allow_html=True)


    st.write("")
    st.divider()

    # ---------- CALL TO ACTION ----------
    st.markdown(
        """
        <h3 style='text-align:center;'>Start exploring your data</h3>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([3,1,3])

    with col2:
        if st.button(" Get Started"):
            st.session_state.page = "chat"
            st.rerun()