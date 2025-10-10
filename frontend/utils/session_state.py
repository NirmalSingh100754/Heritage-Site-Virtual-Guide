import streamlit as st

def init_session_state():
    """Initialize all session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None

def clear_analysis():
    """Clear analysis results"""
    st.session_state.uploaded_image = None
    st.session_state.analysis_result = None

def add_to_chat_history(role: str, message: str):
    """Add message to chat history"""
    st.session_state.chat_history.append({"role": role, "message": message})
    # Keep only last 20 messages
    if len(st.session_state.chat_history) > 20:
        st.session_state.chat_history = st.session_state.chat_history[-20:]