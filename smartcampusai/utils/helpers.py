"""
Helper Utilities Module for SmartCampusAIA.
Provides date formatting, stats extraction, activity log loading, and Plotly visualization builders.
"""

from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List

from utils.database import load_json, ACTIVITY_FILE, SETTINGS_FILE


def format_timestamp(iso_str: str) -> str:
    """Formats an ISO-8601 timestamp string into a human-readable date format."""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%Y-%m-%d %I:%M %p")
    except Exception:
        return iso_str


def get_recent_activities(limit: int = 5) -> List[Dict[str, Any]]:
    """Loads activities and returns the most recent entries."""
    data = load_json(ACTIVITY_FILE, {"activities": []})
    return data.get("activities", [])[:limit]


# --- Plotly Visualization Builders ---

def get_attendance_chart() -> go.Figure:
    """Creates a line chart tracking student attendance trends over the last few days."""
    import streamlit as st
    theme = st.session_state.get("theme", "dark")
    text_color = "#E2E8F0" if theme == "dark" else "#1E293B"
    grid_color = "rgba(255,255,255,0.08)" if theme == "dark" else "rgba(0,0,0,0.08)"
    
    data = load_json(SETTINGS_FILE, {})
    attendance_records = data.get("attendance", [])
    
    if not attendance_records:
        df = pd.DataFrame(columns=["date", "present", "absent", "late"])
    else:
        df = pd.DataFrame(attendance_records)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["present"],
        mode="lines+markers",
        name="Present",
        line=dict(color="#10B981", width=3),
        marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["late"],
        mode="lines+markers",
        name="Late Arrivals",
        line=dict(color="#F59E0B", width=2, dash="dash"),
        marker=dict(size=6)
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["absent"],
        mode="lines+markers",
        name="Absent",
        line=dict(color="#EF4444", width=2, dash="dot"),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title={
            "text": "Daily Attendance Trends",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top"
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color),
        xaxis=dict(gridcolor=grid_color, showgrid=True),
        yaxis=dict(gridcolor=grid_color, showgrid=True),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=30, r=20, t=60, b=30),
        hovermode="x unified"
    )
    return fig


def get_department_distribution_chart() -> go.Figure:
    """Creates a bar chart showcasing student counts per department."""
    import streamlit as st
    theme = st.session_state.get("theme", "dark")
    text_color = "#E2E8F0" if theme == "dark" else "#1E293B"
    grid_color = "rgba(255,255,255,0.08)" if theme == "dark" else "rgba(0,0,0,0.08)"
    
    data = load_json(SETTINGS_FILE, {})
    students = data.get("students", [])
    
    if not students:
        df = pd.DataFrame(columns=["department"])
    else:
        df = pd.DataFrame(students)
        
    dept_counts = df["department"].value_counts().reset_index()
    dept_counts.columns = ["Department", "Count"]

    fig = px.bar(
        dept_counts,
        x="Department",
        y="Count",
        color="Count",
        color_continuous_scale=["#6C63FF", "#8B5CF6", "#A78BFA"],
        title="Student Distribution by Department"
    )
    
    fig.update_layout(
        title_x=0.5,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", showgrid=False),
        yaxis=dict(gridcolor=grid_color, showgrid=True),
        coloraxis_showscale=False,
        margin=dict(l=30, r=20, t=60, b=30)
    )
    return fig


def get_gpa_distribution_chart() -> go.Figure:
    """Creates a histogram representing the GPA distribution of students."""
    import streamlit as st
    theme = st.session_state.get("theme", "dark")
    text_color = "#E2E8F0" if theme == "dark" else "#1E293B"
    grid_color = "rgba(255,255,255,0.08)" if theme == "dark" else "rgba(0,0,0,0.08)"
    
    data = load_json(SETTINGS_FILE, {})
    students = data.get("students", [])
    
    if not students:
        df = pd.DataFrame(columns=["gpa"])
    else:
        df = pd.DataFrame(students)

    fig = px.histogram(
        df,
        x="gpa",
        nbins=10,
        title="Student GPA Distribution",
        color_discrete_sequence=["#10B981"]
    )
    
    fig.update_layout(
        title_x=0.5,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color),
        xaxis=dict(title="GPA", gridcolor=grid_color, showgrid=True),
        yaxis=dict(title="Number of Students", gridcolor=grid_color, showgrid=True),
        margin=dict(l=30, r=20, t=60, b=30),
        bargap=0.05
    )
    return fig


def get_course_pass_rate_chart() -> go.Figure:
    """Creates a polar chart for courses performance / pass rates."""
    import streamlit as st
    theme = st.session_state.get("theme", "dark")
    text_color = "#E2E8F0" if theme == "dark" else "#1E293B"
    grid_color = "rgba(255,255,255,0.08)" if theme == "dark" else "rgba(0,0,0,0.08)"
    
    categories = ["CS-101", "MATH-203", "PHY-102", "CHEM-104", "BUS-301"]
    pass_rates = [94, 88, 76, 85, 90]

    fig = go.Figure(data=go.Scatterpolar(
        r=pass_rates,
        theta=categories,
        fill="toself",
        line_color="#8B5CF6",
        fillcolor="rgba(139, 92, 246, 0.3)"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=grid_color, angle=45, tickfont=dict(color=text_color)),
            angularaxis=dict(gridcolor=grid_color, tickfont=dict(color=text_color))
        ),
        title=dict(text="Course Average Pass Rates (%)", x=0.5),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color),
        margin=dict(l=40, r=40, t=60, b=30)
    )
    return fig
