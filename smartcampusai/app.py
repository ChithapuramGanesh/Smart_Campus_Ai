"""
SmartCampusAIA Main Entrypoint.
Initializes the Streamlit app configuration, custom CSS styling, base64 background assets,
and handles authentication page routing.
"""

import os
import base64
import streamlit as st
from dotenv import load_dotenv

# Set page configuration first (MUST be the first Streamlit command)
st.set_page_config(
    page_title="SmartCampusAIA - Campus Management Dashboard",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load helper modules
from utils.session import initialize_session
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.footer import render_footer
from pages.login import show_login_page
from pages.register import show_register_page
from pages.dashboard import show_dashboard_page

# Load environment variables
load_dotenv()


def get_base64_of_bin_file(bin_file: str) -> str:
    """Reads a binary file and returns its base64 encoded string representation."""
    if not os.path.exists(bin_file):
        return ""
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def apply_custom_assets() -> None:
    """Injects custom CSS and sets the page background image."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Load default styles.css
    css_path = os.path.join(base_dir, "styles", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
    # 2. Inject Theme Overrides for High Legibility and Contrast
    theme = st.session_state.get("theme", "dark")
    if theme == "dark":
        bg_path = os.path.join(base_dir, "assets", "background.png")
        bg_base64 = get_base64_of_bin_file(bg_path)
        
        bg_css_parts = []
        if bg_base64:
            # We add a dark overlay on the background image to ensure texts in front stand out perfectly
            bg_css_parts.append(f"""
            .stApp {{
                background-image: linear-gradient(rgba(15, 15, 26, 0.75), rgba(15, 15, 26, 0.75)), url("data:image/png;base64,{bg_base64}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            """)
        else:
            bg_css_parts.append("""
            .stApp {
                background-color: #0F0F1A !important;
            }
            """)
            
        # Add high contrast dark mode overrides
        bg_css_parts.append("""
        /* Contrast text styling */
        p, li, label, th, td, span, div[data-testid="stMarkdownContainer"] p {
            color: #F8FAFC !important;
            font-size: 1rem;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
        }
        
        /* Make inputs, dropdowns, forms highly readable and distinct */
        input, select, textarea, div[role="button"], div[data-baseweb="select"] {
            color: #FFFFFF !important;
            background-color: #1A1A2E !important;
            border: 1px solid rgba(108, 99, 255, 0.4) !important;
        }
        
        div[data-testid="stForm"] {
            background-color: rgba(26, 26, 46, 0.6) !important;
            border: 1px solid rgba(108, 99, 255, 0.3) !important;
            border-radius: 12px;
            padding: 20px;
        }
        
        /* Highlight metrics inside the cards */
        .metric-value {
            color: #FFFFFF !important;
        }
        
        .metric-label {
            color: #CBD5E1 !important;
        }
        """)
        
        st.markdown(f"<style>{''.join(bg_css_parts)}</style>", unsafe_allow_html=True)
    else:
        # Subtle light theme gradient background with high accessibility contrasts
        light_bg_css = """
        <style>
        .stApp {
            background: linear-gradient(135deg, #F8FAFC, #E2E8F0) !important;
            color: #0F172A !important;
        }
        
        /* High contrast light mode text overrides */
        p, li, label, th, td, span, div[data-testid="stMarkdownContainer"] p {
            color: #1E293B !important;
            font-size: 1rem;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
        }
        
        /* Override dark theme card background and text colors */
        .glass-card {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid rgba(0, 0, 0, 0.12) !important;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.08) !important;
        }
        
        .metric-card {
            background: #FFFFFF !important;
            border: 1px solid rgba(108, 99, 255, 0.25) !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.06) !important;
        }
        
        .metric-label {
            color: #475569 !important;
        }
        
        .chat-assistant {
            background: rgba(0, 0, 0, 0.04) !important;
            border: 1px solid rgba(0, 0, 0, 0.08) !important;
            color: #0F172A !important;
        }
        
        /* Light inputs with dark text */
        input, select, textarea, div[role="button"], div[data-baseweb="select"] {
            color: #0F172A !important;
            background-color: #FFFFFF !important;
            border: 1px solid #94A3B8 !important;
        }
        
        div[data-testid="stForm"] {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 12px;
            padding: 20px;
        }
        </style>
        """
        st.markdown(light_bg_css, unsafe_allow_html=True)


def main() -> None:
    """Core router linking pages and components."""
    # Initialize session variables
    initialize_session()
    
    # Apply modern styles & background
    apply_custom_assets()
    
    logged_in = st.session_state.get("logged_in", False)
    current_page = st.session_state.get("current_page", "Login")

    if logged_in:
        # Renders authenticated workspace layout
        render_navbar()
        
        # Renders custom sidebar and gets selected navigation page
        selected_page = render_sidebar()
        
        # Display the page content viewport
        show_dashboard_page(selected_page)
        
        # Display footer
        render_footer()
    else:
        # Renders public sign-in / registration screens
        if current_page == "Register":
            show_register_page()
        else:
            show_login_page()


if __name__ == "__main__":
    main()
