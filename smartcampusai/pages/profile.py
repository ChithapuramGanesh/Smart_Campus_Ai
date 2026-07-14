"""
Profile Page Module for SmartCampusAIA.
Allows users to modify profile information and update passwords.
"""

import streamlit as st
from utils.auth import update_profile
from utils.helpers import format_timestamp
from utils.database import load_json, ACTIVITY_FILE


def show_profile_page() -> None:
    """Renders the user profile page."""
    user = st.session_state.get("user")
    if not user:
        st.warning("Please log in to view this page.")
        return

    st.markdown('<h1 class="gradient-title">👤 User Profile</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-bottom: 30px;'>Manage your account details and security settings.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Edit Profile Info")
        
        with st.form("profile_update_form"):
            name = st.text_input("Full Name", value=user.get("name", ""))
            email = st.text_input("Email Address", value=user.get("email", ""))
            
            st.markdown("<br/><strong>Change Password (Optional)</strong>", unsafe_allow_html=True)
            new_password = st.text_input("New Password", type="password", placeholder="Leave blank to keep current password")
            
            submitted = st.form_submit_button("Save Changes")
            
            if submitted:
                success, message = update_profile(
                    user_id=user["id"],
                    name=name,
                    email=email,
                    password=new_password if new_password.strip() else None
                )
                if success:
                    st.success(message)
                    # Update active session state
                    user["name"] = name.strip()
                    user["email"] = email.strip().lower()
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(message)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Account Metadata")
        
        created_at_fmt = format_timestamp(user.get("created_at", ""))
        
        st.write(f"**Username:** `{user.get('username')}`")
        st.write(f"**Account ID:** `{user.get('id')}`")
        st.write(f"**Joined On:** {created_at_fmt}")
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'/>", unsafe_allow_html=True)
        st.subheader("Your Recent Activity Log")
        
        # Load activity log matching user
        act_data = load_json(ACTIVITY_FILE, {"activities": []})
        user_acts = [a for a in act_data.get("activities", []) if a.get("username") == user.get("username")]
        
        if not user_acts:
            st.write("_No login or profile changes recorded yet._")
        else:
            for act in user_acts[:3]:
                dt = act.get("timestamp", "").split(".")[0].replace("T", " ")
                st.markdown(
                    f"""
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 8px 12px; border-radius: 6px; margin-bottom: 8px;">
                        <span style="color: #A78BFA; font-size: 0.8rem; font-weight: bold;">{act.get('action')}</span>
                        <div style="font-size: 0.85rem; color: #E2E8F0;">{act.get('details')}</div>
                        <div style="font-size: 0.75rem; color: #64748B;">{dt}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)
