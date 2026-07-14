"""
UI Cards and Widgets Component for SmartCampusAIA.
Provides glassmorphism wrappers, metric groups, notification feeds,
and tabular activity layouts.
"""

import streamlit as st
import textwrap
from typing import List, Dict, Any


def render_glass_card(title: str, content_html: str, theme: str = "dark") -> None:
    """Renders a single content block with glassmorphism CSS classes."""
    card_class = "glass-card-light" if theme == "light" else "glass-card"
    
    html = textwrap.dedent(f"""
    <div class="{card_class}">
        <h3 style="margin-top: 0; margin-bottom: 15px; font-weight: 700; color: #E2E8F0; font-size: 1.25rem; display: flex; align-items: center; gap: 8px;">
            {title}
        </h3>
        <div>
            {content_html}
        </div>
    </div>
    """)
    st.markdown(html, unsafe_allow_html=True)


def render_metrics_cards(metrics: List[Dict[str, Any]]) -> None:
    """
    Renders a row of animated, hover-responsive statistics cards.
    Each item in the metrics list should be a dictionary:
    { "value": "4.0", "label": "GPA", "icon": "🎓" }
    """
    cols = st.columns(len(metrics))
    for i, m in enumerate(metrics):
        val = m.get("value", "")
        lbl = m.get("label", "")
        icon = m.get("icon", "")
        
        with cols[i]:
            card_html = textwrap.dedent(f"""
            <div class="metric-card">
                <div style="font-size: 1.5rem; margin-bottom: 5px;">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{lbl}</div>
            </div>
            """)
            st.markdown(card_html, unsafe_allow_html=True)


def render_notifications(notifications: List[str], theme: str = "dark") -> None:
    """Renders a scrolling or neat vertical stack of system notifications."""
    notif_items = ""
    for n in notifications:
        notif_items += textwrap.dedent(f"""
        <div style="padding: 12px 16px; margin-bottom: 10px; background: rgba(108, 99, 255, 0.05); border-left: 4px solid #6C63FF; border-radius: 4px; font-size: 0.9rem; color: #E2E8F0;">
            🔔 {n}
        </div>
        """)
        
    render_glass_card("Recent Notifications", notif_items, theme)


def render_recent_activities_table(activities: List[Dict[str, Any]], theme: str = "dark") -> None:
    """Renders a responsive summary of logs from users and the campus database."""
    if not activities:
        content = "<p style='color: #94A3B8; font-style: italic;'>No activity logged yet.</p>"
    else:
        rows = ""
        for act in activities:
            timestamp = act.get("timestamp", "")
            # Shorten timestamp for display
            try:
                dt = timestamp.split(".")[0].replace("T", " ")
            except Exception:
                dt = timestamp
                
            rows += textwrap.dedent(f"""
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 10px 8px; font-size: 0.85rem; font-weight: 600; color: #A78BFA;">@{act.get('username')}</td>
                <td style="padding: 10px 8px; font-size: 0.85rem; color: #E2E8F0;"><span style="background: rgba(108, 99, 255, 0.2); color: #C084FC; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem;">{act.get('action')}</span></td>
                <td style="padding: 10px 8px; font-size: 0.85rem; color: #94A3B8;">{act.get('details')}</td>
                <td style="padding: 10px 8px; font-size: 0.80rem; color: #64748B;">{dt}</td>
            </tr>
            """)
            
        content = textwrap.dedent(f"""
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                    <tr style="border-bottom: 2px solid rgba(255,255,255,0.1); color: #94A3B8; font-size: 0.85rem;">
                        <th style="padding: 8px;">User</th>
                        <th style="padding: 8px;">Action</th>
                        <th style="padding: 8px;">Details</th>
                        <th style="padding: 8px;">Date</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """)
    render_glass_card("Recent Campus Logs", content, theme)
