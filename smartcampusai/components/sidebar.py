"""
Sidebar Component for SmartCampusAIA.
Handles navigation options via streamlit-option-menu, shows profile card,
and handles logout triggers.
"""

import streamlit as st
import textwrap
from streamlit_option_menu import option_menu
from utils.session import logout_session


def render_sidebar() -> str:
    """
    Renders the sidebar with school branding, user profile preview,
    and returns the selected page name.
    """
    with st.sidebar:
        # 1. Campus Brand Header
        st.markdown(
            textwrap.dedent("""
            <div style="text-align: center; padding: 15px 0;">
                <h2 style="margin: 0; background: linear-gradient(135deg, #4F46E5, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1.8rem;">SmartCampus</h2>
                <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 5px 0 0 0; letter-spacing: 1.5px; font-weight: 500;">AI ACADEMY</p>
            </div>
            <hr style="border-color: var(--card-border); margin-top: 5px; margin-bottom: 20px;" />
            """),
            unsafe_allow_html=True
        )

        # 2. User Profile Card
        user = st.session_state.get("user")
        if user:
            st.markdown(
                textwrap.dedent(f"""
                <div style="background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 12px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 42px; height: 42px; background: linear-gradient(135deg, #4F46E5, #6366F1); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 1.2rem;">
                            {user['name'][0].upper()}
                        </div>
                        <div>
                            <div style="font-weight: 600; font-size: 0.95rem; color: var(--text-primary);">{user['name']}</div>
                            <div style="font-size: 0.8rem; color: var(--text-secondary);">@{user['username']}</div>
                        </div>
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )

        # 3. Streamlit Option Menu Navigation
        options = ["Dashboard", "AI Assistant", "Students", "Faculty", "Attendance", "Analytics", "Profile", "Settings", "Logout"]
        icons = ["house", "robot", "mortarboard", "person-badge", "calendar-check", "bar-chart", "person", "gear", "box-arrow-right"]
        
        # Calculate selected index based on session state page
        current_page = st.session_state.get("current_page", "Dashboard")
        # In case the current page is stored differently:
        if current_page == "Home":
            current_page = "Dashboard"
        
        try:
            default_index = options.index(current_page)
        except ValueError:
            default_index = 0

        selected = option_menu(
            menu_title=None,  # No title needed, handled by brand header
            options=options,
            icons=icons,
            menu_icon=None,
            default_index=default_index,
            styles={
                "container": {"background-color": "transparent", "padding": "0px"},
                "icon": {"color": "#818CF8", "font-size": "16px"},
                "nav-link": {
                    "font-family": "'Outfit', sans-serif",
                    "font-size": "14px",
                    "color": "var(--text-secondary)",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px 15px",
                    "border-radius": "8px",
                    "--hover-color": "rgba(99, 102, 241, 0.08)",
                    "transition": "all 0.2s ease"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #4F46E5, #6366F1)",
                    "color": "#FFFFFF",
                    "font-weight": "600"
                }
            }
        )

        # 4. Handle Logout Actions immediately in sidebar or return selection
        if selected == "Logout":
            logout_session()
            return "Dashboard"
        
        # If user changed selection, update state
        if selected != current_page:
            st.session_state.current_page = selected
            st.rerun()

        return selected
