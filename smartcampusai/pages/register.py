"""
Register Page Module for SmartCampusAIA.
Handles sign-up forms, strong password policy validation, and user creation.
"""

import streamlit as st
from utils.auth import register_user


def show_register_page() -> None:
    """Renders the user registration interface."""
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-weight: 800; font-size: 2.5rem; background: linear-gradient(45deg, #6C63FF, #A78BFA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px;">Join SmartCampus</h1>
            <p style="color: #94A3B8; font-size: 1rem;">Create an administrative or student workspace account</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, col, right = st.columns([1, 2, 1])
    
    with col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Create Account")
        
        with st.form("register_form", clear_on_submit=False):
            name = st.text_input("Full Name", placeholder="e.g. John Doe")
            email = st.text_input("Email Address", placeholder="e.g. john@example.com")
            username = st.text_input("Username", placeholder="e.g. johndoe")
            password = st.text_input("Password", type="password", placeholder="At least 8 chars, 1 upper, 1 special, 1 number")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat your password")
            
            submitted = st.form_submit_button("Register")
            
            if submitted:
                success, message = register_user(name, email, username, password, confirm_password)
                if success:
                    st.success(message)
                    # Redirect to login page after a brief moment
                    st.session_state.current_page = "Login"
                    st.rerun()
                else:
                    st.error(message)
                    
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Link to login page
        st.markdown(
            """
            <div style="text-align: center; margin-top: 20px;">
                <span style="color: #94A3B8; font-size: 0.9rem;">Already have an account? </span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        if st.button("Sign in to your account", key="switch_to_login"):
            st.session_state.current_page = "Login"
            st.rerun()
