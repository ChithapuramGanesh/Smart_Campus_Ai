"""
Session Management Module for SmartCampusAIA.
Initializes, updates, and tears down Streamlit session states.
"""

import streamlit as st
from typing import Dict, Any, Optional


def initialize_session() -> None:
    """Initializes standard session variables if not already set."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        
    if "user" not in st.session_state:
        st.session_state.user = None
        
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
        
    if "students" not in st.session_state:
        st.session_state.students = []

    if "notifications" not in st.session_state:
        st.session_state.notifications = [
            "AI Assistant version 1.2 deployed.",
            "Mid-term examination schedule released.",
            "System maintenance scheduled for Sunday at 02:00 AM.",
            "Dr. Alan Turing posted a new reading assignment."
        ]


def login_session(user_data: Dict[str, Any]) -> None:
    """Sets session variables upon successful authentication."""
    st.session_state.logged_in = True
    st.session_state.user = user_data
    st.session_state.current_page = "Home"
    # Ensure chat history is reset on new login
    st.session_state.chat_history = []


def logout_session() -> None:
    """Clears authentication details from the session state."""
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.current_page = "Home"
    st.session_state.chat_history = []
    # Rerun the app to update the view
    st.rerun()


def set_page(page_name: str) -> None:
    """Updates the current active page and triggers a rerun."""
    st.session_state.current_page = page_name
    st.rerun()
