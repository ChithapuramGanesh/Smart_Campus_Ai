"""
Navbar Component for SmartCampusAIA.
Displays a brand header, current database state, and session notification indicators.
"""

import streamlit as st
import textwrap


def render_navbar() -> None:
    """Renders the top navigation header bar."""
    user = st.session_state.get("user")
    user_display = f"👤 {user['name']}" if user else "Not Logged In"
    
    navbar_html = textwrap.dedent(f"""
    <div class="header-container">
        <div class="brand-text">
            🏫 <span style="background: linear-gradient(45deg, #6C63FF, #A78BFA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">SmartCampus</span> AIA
        </div>
        <div style="display: flex; align-items: center; gap: 15px; font-weight: 500; font-size: 0.95rem; color: #94A3B8;">
            <span>🟢 System: Operational</span>
            <span style="color: #6C63FF; font-weight: 600;">{user_display}</span>
        </div>
    </div>
    """)
    st.markdown(navbar_html, unsafe_allow_html=True)
