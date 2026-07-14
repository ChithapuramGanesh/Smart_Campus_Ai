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
            # Subtle gradient overlay over our premium mesh image
            bg_css_parts.append(f"""
            .stApp {{
                background-image: linear-gradient(rgba(9, 11, 16, 0.8), rgba(9, 11, 16, 0.88)), url("data:image/png;base64,{bg_base64}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            """)
        else:
            bg_css_parts.append("""
            .stApp {
                background: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                            radial-gradient(circle at 90% 80%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
                            #090B10 !important;
            }
            """)
            
        bg_css_parts.append("""
        /* Light/Dark specific setup */
        .stApp {
            color: var(--text-primary);
        }
        
        /* Contrast text styling for markdown/general elements */
        div[data-testid="stMarkdownContainer"] p, 
        div[data-testid="stMarkdownContainer"] li {
            color: var(--text-secondary);
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
        }
        
        /* Make inputs, dropdowns, forms highly readable and distinct */
        input, select, textarea, div[role="button"], div[data-baseweb="select"] {
            color: var(--text-primary) !important;
            background-color: var(--input-bg) !important;
            border: 1px solid var(--input-border) !important;
        }
        
        input:focus, select:focus, textarea:focus {
            border-color: var(--accent-indigo) !important;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
        }
        
        div[data-testid="stForm"] {
            background-color: rgba(20, 24, 37, 0.5) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15) !important;
        }
        """)
        
        st.markdown(f"<style>{''.join(bg_css_parts)}</style>", unsafe_allow_html=True)
    else:
        # Subtle light theme gradient background with high accessibility contrasts
        light_bg_css = """
        <style>
        .stApp {
            --bg-primary: #F8FAFC;
            --bg-secondary: #F1F5F9;
            --card-bg: rgba(255, 255, 255, 0.75);
            --card-border: rgba(0, 0, 0, 0.04);
            --card-hover-border: rgba(79, 70, 229, 0.2);
            --card-hover-shadow: rgba(79, 70, 229, 0.06);
            
            --text-primary: #0F172A;
            --text-secondary: #475569;
            --text-muted: #94A3B8;
            
            --input-bg: #FFFFFF;
            --input-border: #E2E8F0;
            
            background: linear-gradient(135deg, #F8FAFC, #F1F5F9) !important;
            color: #0F172A !important;
        }
        
        /* Light mode text overrides */
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li {
            color: #475569 !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
        }
        
        /* Override dark theme card background and text colors */
        .glass-card {
            background: rgba(255, 255, 255, 0.75) !important;
            border: 1px solid rgba(0, 0, 0, 0.04) !important;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.04) !important;
        }
        
        .metric-card {
            background: #FFFFFF !important;
            border: 1px solid rgba(79, 70, 229, 0.12) !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
        }
        
        .metric-label {
            color: #64748B !important;
        }
        
        .chat-assistant {
            background: rgba(0, 0, 0, 0.02) !important;
            border: 1px solid rgba(0, 0, 0, 0.04) !important;
            color: #0F172A !important;
        }
        
        /* Light inputs with dark text */
        input, select, textarea, div[role="button"], div[data-baseweb="select"] {
            color: #0F172A !important;
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
        }
        
        div[data-testid="stForm"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.04) !important;
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
