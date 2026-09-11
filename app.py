import streamlit as st

from database import create_database


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="CampusIQ",
    page_icon="🏫",
    layout="wide"
)


# -----------------------------
# Create Database
# -----------------------------

create_database()


# -----------------------------
# Custom Header
# -----------------------------

st.markdown("""
<div style="
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    padding: 35px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 25px;
">

<h1 style="
    color: white !important;
    margin: 0;
    font-size: 38px;
">
🏫 CampusIQ
</h1>

<p style="
    color: #F5F3FF !important;
    font-size: 18px;
    margin: 8px 0 0 0;
">
AI-Powered Campus Problem Intelligence System
</p>

</div>
""", unsafe_allow_html=True)


# -----------------------------
# Description
# -----------------------------

st.markdown("""
<p style="
    text-align: center;
    font-size: 17px;
    color: #687280;
">
A centralized platform to report, analyze, prioritize, assign
and resolve campus problems.
</p>
""", unsafe_allow_html=True)


st.divider()


# -----------------------------
# How CampusIQ Works
# -----------------------------

st.header("🚀 How CampusIQ Works")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.subheader("📝 Report")

    st.write(
        "Students and faculty report campus issues "
        "with location and problem details."
    )


with col2:

    st.subheader("🤖 Analyze")

    st.write(
        "AI analyzes the complaint and predicts "
        "its category and priority."
    )


with col3:

    st.subheader("🏢 Assign")

    st.write(
        "CampusIQ recommends the responsible "
        "department for handling the issue."
    )


with col4:

    st.subheader("📊 Resolve")

    st.write(
        "Administrators track complaints and "
        "monitor their resolution."
    )


st.divider()


# -----------------------------
# Key Features
# -----------------------------

st.header("✨ Key Features")


feature_col1, feature_col2, feature_col3 = st.columns(3)


with feature_col1:

    st.info(
        "🤖 **AI-Powered Analysis**\n\n"
        "Automatic category prediction, "
        "confidence scoring and priority detection."
    )


with feature_col2:

    st.info(
        "🔄 **Recurring Issue Detection**\n\n"
        "Identifies similar complaints to reveal "
        "recurring campus problems."
    )


with feature_col3:

    st.info(
        "📊 **Smart Analytics Dashboard**\n\n"
        "Interactive insights about categories, "
        "locations, departments and resolution status."
    )


st.divider()


# -----------------------------
# Navigation Message
# -----------------------------

st.success(
    "👈 Use the sidebar to **Report a Problem** "
    "or open the **Admin Dashboard**."
)