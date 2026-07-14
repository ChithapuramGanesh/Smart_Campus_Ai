"""
Footer Component for SmartCampusAIA.
Renders the standard footer markup at the bottom of pages.
"""

import streamlit as st
import textwrap


def render_footer() -> None:
    """Renders the dashboard footer section."""
    footer_html = textwrap.dedent("""
    <hr style="border-color: rgba(255,255,255,0.05); margin-top: 50px; margin-bottom: 20px;" />
    <div style="text-align: center; color: #64748B; font-size: 0.85rem; padding-bottom: 20px; font-weight: 500;">
        SmartCampusAIA © 2026. Made with Python & Streamlit. Powered by OpenAI.
    </div>
    """)
    st.markdown(footer_html, unsafe_allow_html=True)
