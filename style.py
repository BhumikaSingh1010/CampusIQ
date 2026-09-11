import streamlit as st


def apply_style():

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #F7F8FC;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }

        section[data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid #E5E7EB;
        }

        h1, h2, h3 {
            color: #1F2937 !important;
            font-weight: 700 !important;
        }

        p, label, span {
            color: #374151;
        }

        input, textarea {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
        }

        div[data-baseweb="input"],
        div[data-baseweb="select"],
        div[data-baseweb="textarea"] {
            background-color: #FFFFFF !important;
            border-radius: 10px !important;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            background: #6C63FF;
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            background: #584FE0;
        }

        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            padding: 18px;
            border-radius: 14px;
            box-shadow: 0 3px 12px rgba(0,0,0,0.04);
        }

        </style>
        """,
        unsafe_allow_html=True
    )