"""
Settings Page Module for SmartCampusAIA.
Manages API key custom configurations, theme selections, and account deletion.
"""

import os
import streamlit as st
from utils.auth import delete_user
from utils.session import logout_session
from utils.ai import test_api_connection, get_api_credentials


def show_settings_page() -> None:
    """Renders the settings panel."""
    user = st.session_state.get("user")
    if not user:
        st.warning("Please log in to view this page.")
        return

    st.markdown('<h1 class="gradient-title">⚙ Settings</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-bottom: 30px;'>Manage application preferences and system integrations.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("OpenAI API Integration")
        
        # Display current active settings
        curr_key, curr_model, curr_base = get_api_credentials()
        masked_key = f"{curr_key[:6]}...{curr_key[-4:]}" if len(curr_key) > 10 else "Not set (Mockup mode active)"
        
        st.info(f"**Current Active Model:** `{curr_model}`\n\n**API Key status:** `{masked_key}`")
        
        # Allow user to update settings
        new_key = st.text_input("Custom OpenAI API Key", type="password", 
                               value=st.session_state.get("custom_api_key", ""), 
                               placeholder="sk-...")
        
        new_model = st.text_input("Model Name", 
                                 value=st.session_state.get("custom_model_name", "gpt-4o-mini"),
                                 placeholder="e.g. gpt-4o-mini")
        
        cols = st.columns([1, 1])
        with cols[0]:
            if st.button("Apply API Settings"):
                st.session_state.custom_api_key = new_key.strip()
                st.session_state.custom_model_name = new_model.strip()
                st.success("API preferences updated!")
                st.rerun()
                
        with cols[1]:
            if st.button("Verify Connection"):
                if not new_key.strip():
                    st.warning("Please enter a key to verify.")
                else:
                    with st.spinner("Testing API connection..."):
                        success, msg = test_api_connection(new_key.strip(), new_model.strip(), curr_base)
                        if success:
                            st.success("Connection verified successfully! Your key is valid.")
                        else:
                            st.error(f"Verification failed: {msg}")
                            
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Theme & Visual Preferences")
        theme_options = ["dark", "light"]
        current_theme = st.session_state.get("theme", "dark")
        try:
            theme_idx = theme_options.index(current_theme)
        except ValueError:
            theme_idx = 0
            
        selected_theme = st.selectbox("Dashboard Theme Mode", theme_options, index=theme_idx)
        if selected_theme != current_theme:
            st.session_state.theme = selected_theme
            st.success(f"Theme mode switched to {selected_theme}!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card" style="border: 1px solid rgba(239, 68, 68, 0.3);">', unsafe_allow_html=True)
        st.subheader("🚨 Danger Zone")
        st.write("Account actions in this section are permanent and cannot be undone.")
        
        st.warning("Deleting your account will purge all personal credentials, logs, and settings data.")
        
        confirm = st.checkbox("I confirm that I want to delete my account permanently.")
        
        if st.button("Delete My Account", type="primary", disabled=not confirm):
            success = delete_user(user["id"])
            if success:
                st.success("Your account has been deleted. Logging out...")
                logout_session()
            else:
                st.error("Failed to delete account. Please try again.")
        st.markdown('</div>', unsafe_allow_html=True)
