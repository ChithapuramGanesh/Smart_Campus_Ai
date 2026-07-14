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
        <h3 style="margin-top: 0; margin-bottom: 15px; font-weight: 700; color: var(--text-primary); font-size: 1.25rem; display: flex; align-items: center; gap: 8px;">
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
        <div style="padding: 12px 16px; margin-bottom: 10px; background: rgba(99, 102, 241, 0.05); border-left: 4px solid var(--primary-indigo); border-radius: 8px; font-size: 0.9rem; color: var(--text-primary);">
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
            <tr style="border-bottom: 1px solid var(--card-border);">
                <td style="padding: 10px 8px; font-size: 0.85rem; font-weight: 600; color: var(--accent-light);">@{act.get('username')}</td>
                <td style="padding: 10px 8px; font-size: 0.85rem; color: var(--text-primary);"><span style="background: rgba(99, 102, 241, 0.15); color: var(--accent-light); padding: 2.5px 7px; border-radius: 6px; font-size: 0.75rem;">{act.get('action')}</span></td>
                <td style="padding: 10px 8px; font-size: 0.85rem; color: var(--text-secondary);">{act.get('details')}</td>
                <td style="padding: 10px 8px; font-size: 0.80rem; color: var(--text-muted);">{dt}</td>
            </tr>
            """)
            
        content = textwrap.dedent(f"""
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                    <tr style="border-bottom: 2px solid var(--card-border); color: var(--text-secondary); font-size: 0.85rem;">
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
