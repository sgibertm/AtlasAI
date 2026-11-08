# =============================================================================
# MAIN APPLICATION: Root controller for the Atlas AI Travel Advisor.
# 1. Configures global page settings, custom CSS themes, and session states.
# 2. Implements a sidebar for real-time user profile tracking and progress.
# 3. Manages high-level routing between the Chat and Recommendation views.
#
# Authors:  Alex Vilamitjana, Sara Gibert, Oriol Pros
# Subject:  Knowledge-Based Systems
# =============================================================================

import streamlit as st

from nav.chat import chat
from nav.recommendations import recommendations
from nav.utils import number_questions

# Page Configuration
st.set_page_config(
    page_title="Atlas AI", 
    page_icon="img/logo.png", 
    layout="wide"
)

st.logo("img/logo.png")

# Global Styles (CSS)
st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #D3e4ff;
    }
    
    /* Button base */
    .stButton > button {
        font-weight: 600;
        transition: all 0.2s;
        background-color: #d3e4ff;
    }
    
    /* Primary (dark blue -> active) */
    .stButton > button[kind="primary"] {
        background-color: #1d4ed8 !important;
        color: white !important;
        border: none;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #1e40af !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3);
    }
    
    /* Secondary (light blue -> inactive) */
    .stButton > button[kind="secondary"] {
        background-color: #3b82f6 !important;
        color: white !important;
        opacity: 0.85;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: #2563eb !important;
        transform: translateY(-1px);
    }
        
    [data-testid="stChatMessage"] {
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 10px;
        max-width: 80%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background-color: #d3e4ff;
        margin-left: auto; 
        flex-direction: row-reverse; 
        border-bottom-right-radius: 2px; 
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "step" not in st.session_state:
    st.session_state.step = 0
if "chat" not in st.session_state:
    st.session_state.chat = []
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "page" not in st.session_state:
    st.session_state.page = "chat"


# Sidebar Information
with st.sidebar:
    st.image("img/logotype_atlas.png", use_container_width=True)
    st.divider()
    
    st.subheader("Your Progress")
    total_questions = number_questions()
    progress_percentage = min(st.session_state.step / total_questions, 1.0)
    
    st.markdown("""
        <style>
        .stProgress > div > div > div > div {
            background-color: #1d4ed8; 
        }
        </style>
    """, unsafe_allow_html=True)

    st.progress(progress_percentage)
    st.caption(f"Question {st.session_state.step} of {total_questions}")

    st.divider()

    st.subheader("Current Profile")
    if st.session_state.responses:
        for key, value in st.session_state.responses.items():

            label = key.replace('_', ' ').title()
            
            # Ensure we display a string
            if isinstance(value, str):
                display_value = value
            else:
                ", ".join(value).title()
            
            st.write(f"**{label}:** {display_value}")
    else:
        st.info("I'm waiting for your answers to build your profile...")

    st.divider()
    
    if st.button("Reset Conversation", use_container_width=True):
        st.session_state.step = 0
        st.session_state.chat = []
        st.session_state.responses = {}
        st.rerun()


col1, col2 = st.columns(2)

with col1:
    if st.button("Atlas AI", use_container_width=True, type = "primary" if st.session_state.page == "chat" else "secondary"):
        st.session_state.page = "chat"
        st.rerun()
with col2:
    if st.button("Recommendations", use_container_width=True, type = "primary" if st.session_state.page == "recommendation" else "secondary"):
        st.session_state.page = "recommendation"
        st.rerun()


if st.session_state.page == "chat":
    chat()
elif st.session_state.page == "recommendation":
    recommendations()


st.markdown("""
    <p style="text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 2rem;">
        Atlas Vacation Logic © 2026 | Version 1.0
    </p>
""", unsafe_allow_html=True)
