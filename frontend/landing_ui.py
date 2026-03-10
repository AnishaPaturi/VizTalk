
import streamlit as st

def render_landing():

    # ---------- HERO SECTION ----------
    col1, col2 = st.columns([8,1])

    with col2:
        if st.button("Login / Register"):
            st.session_state.page = "login"
            st.rerun()

    st.markdown(
        """
        <h1 style='text-align:center;'>VizTalk!</h1>
        """,
        unsafe_allow_html=True
    )

    # st.markdown(
    #     """
    #     <p style='text-align:center; font-size:18px;'>
    #     Ask questions and instantly get insights and visualizations about your data.
    #     </p>
    #     """,
    #     unsafe_allow_html=True
    # )
    st.markdown("""
<marquee behavior="scroll" direction="left" scrollamount="6"
style="
font-size:18px;
font-weight:500;
color:#1B263B;
margin-top:10px;
margin-bottom:10px;">
Ask questions and instantly get insights and visualizations about your data • Explore datasets using natural language • Generate dashboards instantly
</marquee>
""", unsafe_allow_html=True)

    st.markdown(
        """
        <p style='text-align:center; font-size:16px; color:gray;'>
        This platform allows users to explore datasets using natural language.
        Simply type your question and the system automatically generates charts,
        metrics, and dashboards to help you understand your data quickly.
        </p>
        """,
        unsafe_allow_html=True
    )

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

    # ---------- FEATURES ----------
    # st.subheader("Key Features")

    # col1, col2 = st.columns(2)

    # with col1:
    #     st.markdown("💬 **Natural Language Queries**")
    #     st.write("Ask questions about your data in plain English without writing SQL.")

    #     st.markdown("📊 **Automatic Dashboard Generation**")
    #     st.write("Charts and insights are automatically created based on your query.")

    # with col2:
    #     st.markdown("🎤 **Voice Queries**")
    #     st.write("Ask questions using voice commands.")

    #     st.markdown("📁 **Dataset Upload**")
    #     st.write("Upload your own dataset and instantly explore insights.")


    st.subheader("Key Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
    <div style="
    border:1px solid #e6e6e6;
    padding:20px;
    border-radius:10px;
    margin-bottom:15px;
    background-color:#f9f9f9;
    color:black;">    
    <h4>💬 Natural Language Queries</h4>
    <p>Ask questions about your data in plain English without writing SQL.</p>
    </div>
    """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
        border:1px solid #e6e6e6;
        padding:20px;
        border-radius:10px;
        background-color:#f9f9f9;
        color:black;">
        <h4>📊 Automatic Dashboard Generation</h4>
        <p>Charts and insights are automatically created based on your query.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
        border:1px solid #e6e6e6;
        padding:20px;
        border-radius:10px;
        margin-bottom:15px;
        background-color:#f9f9f9;
        color:black;">
        <h4>🎤 Voice Queries</h4>
        <p>Ask questions using voice commands.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
        border:1px solid #e6e6e6;
        padding:10px;
        border-radius:10px;
        background-color:#f9f9f9;
        color:black;">
        <h4>📁 Dataset Upload</h4>
        <p>Upload your own dataset and instantly explore insights.</p>
        </div>
        """, unsafe_allow_html=True)
    st.write("")
    st.divider()

    # ---------- HOW IT WORKS ----------
    st.subheader("How It Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**1️⃣ Upload Dataset**")
        st.write("Upload a CSV dataset to begin analysis.")

    with col2:
        st.markdown("**2️⃣ Ask a Question**")
        st.write("Ask questions in natural language.")

    with col3:
        st.markdown("**3️⃣ View Insights**")
        st.write("Instantly get charts, metrics, and dashboards.")

    st.write("")
    st.divider()

    # ---------- EXAMPLE QUERIES ----------
    st.subheader("Example Queries")

    st.markdown(
        """
        • Show revenue by campaign type  
        • Show monthly revenue trends  
        • Compare marketing channel performance  
        • Show top performing products  
        """
    )

    st.write("")
    st.divider()

    # ---------- CALL TO ACTION ----------
    st.markdown(
        """
        <h3 style='text-align:center;'>Start exploring your data today</h3>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([3,1,3])

    with col2:
        if st.button(" Get Started"):
            st.session_state.page = "chat"
            st.rerun()