"""
Login Page Module for SmartCampusAIA.
Handles authentication form rendering, credential verification, and routing transitions.
"""

import streamlit as st
from utils.auth import authenticate_user
from utils.session import login_session


def show_login_page() -> None:
    """Renders the secure user login interface."""
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-weight: 800; font-size: 2.5rem; background: linear-gradient(135deg, #4F46E5, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px;">Welcome Back</h1>
            <p style="color: var(--text-secondary); font-size: 1rem;">SmartCampus AIA Management Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Wrap in a center column for layout aesthetics
    left, col, right = st.columns([1, 2, 1])
    
    with col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Login to Account")
        
        with st.form("login_form", clear_on_submit=False):
            username_or_email = st.text_input("Username or Email", placeholder="e.g. john or john@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            remember_me = st.checkbox("Remember session", value=True)
            
            submitted = st.form_submit_button("Sign In")
            
            if submitted:
                if not username_or_email.strip() or not password:
                    st.error("Please fill in all fields.")
                else:
                    user = authenticate_user(username_or_email, password)
                    if user:
                        st.success(f"Success! Welcome, {user['name']}.")
                        login_session(user)
                        st.rerun()
                    else:
                        st.error("Invalid Username/Email or Password.")
                        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Link to registration page
        st.markdown(
            """
            <div style="text-align: center; margin-top: 20px;">
                <span style="color: var(--text-secondary); font-size: 0.9rem;">New to the platform? </span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        if st.button("Create a new account", key="switch_to_register"):
            st.session_state.current_page = "Register"
            st.rerun()
