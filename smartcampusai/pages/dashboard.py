"""
Dashboard Router and Sub-Pages Module for SmartCampusAIA.
Implements Home, AI Chat, Students, Faculty, Attendance, and Analytics views.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from components.cards import (
    render_glass_card,
    render_metrics_cards,
    render_notifications,
    render_recent_activities_table
)
from utils.database import load_json, save_json, SETTINGS_FILE, log_activity
from utils.helpers import (
    get_recent_activities,
    get_attendance_chart,
    get_department_distribution_chart,
    get_gpa_distribution_chart,
    get_course_pass_rate_chart
)
from utils.ai import get_ai_chat_response

# Import sub-pages directly for clean routing
from pages.profile import show_profile_page
from pages.settings import show_settings_page


def show_dashboard_page(page_name: str) -> None:
    """Routes to the active dashboard sub-page view."""
    theme = st.session_state.get("theme", "dark")
    user = st.session_state.get("user")
    
    if not user:
        st.warning("Please log in to continue.")
        return

    # Route based on navigation page name
    if page_name == "Dashboard":
        render_home_view(user, theme)
    elif page_name == "AI Assistant":
        render_ai_chat_view(theme)
    elif page_name == "Students":
        render_students_view(theme)
    elif page_name == "Faculty":
        render_faculty_view(theme)
    elif page_name == "Attendance":
        render_attendance_view(theme)
    elif page_name == "Analytics":
        render_analytics_view(theme)
    elif page_name == "Profile":
        show_profile_page()
    elif page_name == "Settings":
        show_settings_page()


# --- 1. HOME VIEW ---

def render_home_view(user: dict, theme: str) -> None:
    """Renders the dashboard home summary view."""
    st.markdown(f'<h1 class="gradient-title">🏫 Welcome, {user.get("name")}!</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-bottom: 25px;'>Here is a summary of the SmartCampus status for today.</p>", unsafe_allow_html=True)

    # Load stats from database
    db_data = load_json(SETTINGS_FILE, {})
    students_count = len(db_data.get("students", []))
    faculty_count = len(db_data.get("faculty", []))
    
    # Calculate attendance average for the last entry
    attendance_records = db_data.get("attendance", [])
    latest_present = 0
    latest_absent = 0
    if attendance_records:
        latest = attendance_records[-1]
        latest_present = latest.get("present", 0)
        latest_absent = latest.get("absent", 0)
        
    total_expected = latest_present + latest_absent
    attendance_rate = f"{(latest_present / total_expected * 100):.1f}%" if total_expected > 0 else "N/A"

    # Render statistics row
    metrics = [
        {"value": str(students_count), "label": "Enrolled Students", "icon": "👨‍🎓"},
        {"value": str(faculty_count), "label": "Active Faculty", "icon": "👩‍🏫"},
        {"value": attendance_rate, "label": "Today's Attendance", "icon": "📈"},
        {"value": "Healthy", "label": "System Status", "icon": "⚡"}
    ]
    render_metrics_cards(metrics)
    
    st.markdown("<br/>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Visual chart
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Attendance Overview")
        fig = get_attendance_chart()
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Recent activities table
        recent_acts = get_recent_activities(5)
        render_recent_activities_table(recent_acts, theme)

    with col2:
        # Notifications Feed
        notifs = st.session_state.get("notifications", [])
        render_notifications(notifs, theme)

        # AI Assistant Quick Widget
        st.markdown('<div class="glass-card" style="border-color: rgba(139, 92, 246, 0.35);">', unsafe_allow_html=True)
        st.subheader("🤖 Quick AI Ask")
        st.write("Need quick information about classes, faculty offices, or GPA trends?")
        quick_query = st.text_input("Ask AI Assistant:", placeholder="Type a campus question...", label_visibility="collapsed")
        
        if quick_query:
            st.session_state.current_page = "AI Assistant"
            # Populate chat history with user question
            st.session_state.chat_history.append({"role": "user", "content": quick_query})
            # Trigger page change
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# --- 2. AI ASSISTANT VIEW ---

def render_ai_chat_view(theme: str) -> None:
    """Renders the full conversational chatbot page."""
    st.markdown('<h1 class="gradient-title">🤖 AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-bottom: 25px;'>Ask general questions or query local databases (Mock engine will reply if API Key is not set).</p>", unsafe_allow_html=True)

    # Initialize chat history or get from session
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_history = st.session_state.chat_history

    # Clear chat utility
    col_title, col_btn = st.columns([5, 1])
    with col_btn:
        if st.button("Clear History", key="clear_chat_history"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()

    # Container to show chat history scroll
    st.markdown('<div class="glass-card" style="min-height: 400px; padding: 20px;">', unsafe_allow_html=True)
    
    if not chat_history:
        st.info("Start the conversation by typing your message below! Ask me about student lists, faculty details, or campus attendance.")
    else:
        for msg in chat_history:
            bubble_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
            sender_label = "👤 **You**" if msg["role"] == "user" else "🤖 **SmartCampus AI**"
            st.markdown(
                f"""
                <div class="chat-bubble {bubble_class}">
                    <div style="font-size:0.85rem; opacity:0.8; margin-bottom:5px;">{sender_label}</div>
                    <div>{msg['content']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input form
    with st.form("chat_input_form", clear_on_submit=True):
        user_message = st.text_input("Message...", placeholder="Ask a question...")
        send_btn = st.form_submit_button("Send")
        
        if send_btn and user_message.strip():
            # Append user message
            st.session_state.chat_history.append({"role": "user", "content": user_message.strip()})
            st.rerun()

    # Handle generating response if last message is from user
    if chat_history and chat_history[-1]["role"] == "user":
        with st.spinner("AI is thinking..."):
            response_generator = get_ai_chat_response(chat_history)
            
            # Since Streamlit forms block reruns and we want a streaming effect, we can run it here
            full_response = ""
            response_placeholder = st.empty()
            
            for chunk in response_generator:
                full_response += chunk
                response_placeholder.markdown(
                    f"""
                    <div class="chat-bubble chat-assistant" style="margin-top:10px;">
                        <div style="font-size:0.85rem; opacity:0.8; margin-bottom:5px;">🤖 **SmartCampus AI (Streaming...)**</div>
                        <div>{full_response}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            # Append full response
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            st.rerun()


# --- 3. STUDENTS MANAGER VIEW ---

def render_students_view(theme: str) -> None:
    """Renders the student roster, search tools, and registration controls."""
    st.markdown('<h1 class="gradient-title">👨‍🎓 Students Directory</h1>', unsafe_allow_html=True)
    
    db_data = load_json(SETTINGS_FILE, {})
    students = db_data.get("students", [])

    # Split workspace layout
    col_list, col_add = st.columns([2, 1])

    with col_list:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Student Roster")
        
        search_query = st.text_input("Search Students", placeholder="Search by name, ID, or department...").lower()
        
        filtered_students = students
        if search_query:
            filtered_students = [
                s for s in students
                if search_query in s["name"].lower()
                or search_query in s["id"].lower()
                or search_query in s["department"].lower()
            ]

        if not filtered_students:
            st.write("_No students found matching filters._")
        else:
            df = pd.DataFrame(filtered_students)
            # Reorder columns
            df = df[["id", "name", "email", "department", "gpa", "status"]]
            df.columns = ["Student ID", "Full Name", "Email Address", "Department", "GPA Score", "Status"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_add:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Register New Student")
        
        with st.form("add_student_form", clear_on_submit=True):
            stu_id = st.text_input("Student ID", placeholder="e.g. STU006")
            stu_name = st.text_input("Full Name", placeholder="e.g. John Doe")
            stu_email = st.text_input("Email", placeholder="e.g. john@smartcampus.edu")
            stu_dept = st.selectbox("Department", ["Computer Science", "Mathematics", "Physics", "Chemistry", "Cybernetics", "Archaeology", "Business & Engineering"])
            stu_gpa = st.number_input("GPA", min_value=0.0, max_value=4.0, value=3.0, step=0.1)
            stu_status = st.selectbox("Status", ["Active", "On Leave", "Graduated"])
            
            submitted = st.form_submit_button("Add Student")
            
            if submitted:
                # Validation checks
                if not stu_id.strip() or not stu_name.strip() or not stu_email.strip():
                    st.error("All fields are required.")
                elif any(s["id"] == stu_id.strip() for s in students):
                    st.error("Student ID already exists.")
                elif any(s["email"] == stu_email.strip() for s in students):
                    st.error("Email Address already registered.")
                else:
                    new_student = {
                        "id": stu_id.strip(),
                        "name": stu_name.strip(),
                        "email": stu_email.strip(),
                        "department": stu_dept,
                        "gpa": float(stu_gpa),
                        "status": stu_status
                    }
                    students.append(new_student)
                    db_data["students"] = students
                    
                    if save_json(SETTINGS_FILE, db_data):
                        st.success(f"Success! {stu_name} registered.")
                        log_activity(st.session_state.user["username"], "Add Student", f"Registered new student: {stu_name} ({stu_id})")
                        st.rerun()
                    else:
                        st.error("Failed to save changes.")
                        
        st.markdown('</div>', unsafe_allow_html=True)


# --- 4. FACULTY DIRECTORY VIEW ---

def render_faculty_view(theme: str) -> None:
    """Renders the faculty staff directory and office details."""
    st.markdown('<h1 class="gradient-title">👩‍🏫 Faculty Directory</h1>', unsafe_allow_html=True)
    
    db_data = load_json(SETTINGS_FILE, {})
    faculty = db_data.get("faculty", [])

    col_list, col_add = st.columns([2, 1])

    with col_list:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Faculty & Staff Directory")
        
        search_query = st.text_input("Search Faculty", placeholder="Search by name, department, or designation...").lower()
        
        filtered_faculty = faculty
        if search_query:
            filtered_faculty = [
                f for f in faculty
                if search_query in f["name"].lower()
                or search_query in f["department"].lower()
                or search_query in f["designation"].lower()
            ]

        if not filtered_faculty:
            st.write("_No faculty members found matching search query._")
        else:
            df = pd.DataFrame(filtered_faculty)
            df = df[["id", "name", "email", "department", "designation", "office"]]
            df.columns = ["Faculty ID", "Name", "Email Address", "Department", "Designation", "Office Room"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_add:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Add Faculty Member")
        
        with st.form("add_faculty_form", clear_on_submit=True):
            fac_id = st.text_input("Faculty ID", placeholder="e.g. FAC005")
            fac_name = st.text_input("Full Name", placeholder="e.g. Dr. Jane Goodall")
            fac_email = st.text_input("Email", placeholder="e.g. jane@smartcampus.edu")
            fac_dept = st.selectbox("Department", ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology", "Cybernetics", "Business & Engineering"])
            fac_desg = st.text_input("Designation", placeholder="e.g. Professor")
            fac_office = st.text_input("Office Room", placeholder="e.g. Room 502")
            
            submitted = st.form_submit_button("Add Member")
            
            if submitted:
                if not fac_id.strip() or not fac_name.strip() or not fac_email.strip():
                    st.error("ID, Name, and Email are required.")
                elif any(f["id"] == fac_id.strip() for f in faculty):
                    st.error("Faculty ID already exists.")
                else:
                    new_member = {
                        "id": fac_id.strip(),
                        "name": fac_name.strip(),
                        "email": fac_email.strip(),
                        "department": fac_dept,
                        "designation": fac_desg.strip(),
                        "office": fac_office.strip()
                    }
                    faculty.append(new_member)
                    db_data["faculty"] = faculty
                    
                    if save_json(SETTINGS_FILE, db_data):
                        st.success(f"Success! Faculty member {fac_name} added.")
                        log_activity(st.session_state.user["username"], "Add Faculty", f"Added faculty member: {fac_name} ({fac_id})")
                        st.rerun()
                    else:
                        st.error("Failed to save changes.")
                        
        st.markdown('</div>', unsafe_allow_html=True)


# --- 5. ATTENDANCE VIEW ---

def render_attendance_view(theme: str) -> None:
    """Renders records of attendance and a logging dashboard."""
    st.markdown('<h1 class="gradient-title">📈 Attendance Tracker</h1>', unsafe_allow_html=True)
    
    db_data = load_json(SETTINGS_FILE, {})
    attendance = db_data.get("attendance", [])

    col_chart, col_log = st.columns([2, 1])

    with col_chart:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Attendance History Trends")
        fig = get_attendance_chart()
        st.plotly_chart(fig, use_container_width=True)
        
        # Display as table
        if attendance:
            df = pd.DataFrame(attendance)
            df = df.iloc[::-1]  # Reverse for latest first
            df.columns = ["Record Date", "Present Students", "Absent Students", "Late Arrivals"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_log:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Log Today's Roll Call")
        
        with st.form("log_attendance_form", clear_on_submit=True):
            today_date = st.date_input("Report Date", value=datetime.today())
            num_present = st.number_input("Present Students", min_value=0, value=400, step=5)
            num_absent = st.number_input("Absent Students", min_value=0, value=20, step=2)
            num_late = st.number_input("Late Arrivals", min_value=0, value=10, step=1)
            
            submitted = st.form_submit_button("Submit Record")
            
            if submitted:
                date_str = today_date.strftime("%Y-%m-%d")
                
                # If date already exists, overwrite, otherwise append
                existing_idx = -1
                for idx, r in enumerate(attendance):
                    if r["date"] == date_str:
                        existing_idx = idx
                        break
                        
                new_record = {
                    "date": date_str,
                    "present": int(num_present),
                    "absent": int(num_absent),
                    "late": int(num_late)
                }
                
                if existing_idx != -1:
                    attendance[existing_idx] = new_record
                else:
                    attendance.append(new_record)
                    
                # Re-sort attendance list by date chronologically
                attendance.sort(key=lambda x: x["date"])
                db_data["attendance"] = attendance
                
                if save_json(SETTINGS_FILE, db_data):
                    st.success(f"Roll call submitted for {date_str}.")
                    log_activity(st.session_state.user["username"], "Log Attendance", f"Submitted attendance logs for {date_str}.")
                    st.rerun()
                else:
                    st.error("Failed to save changes.")
                    
        st.markdown('</div>', unsafe_allow_html=True)


# --- 6. ANALYTICS VIEW ---

def render_analytics_view(theme: str) -> None:
    """Renders all statistical charts and campus demographic maps."""
    st.markdown('<h1 class="gradient-title">📊 Campus Analytics</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-bottom: 25px;'>Visual breakdown of department, grade performance, and metrics.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig_dept = get_department_distribution_chart()
        st.plotly_chart(fig_dept, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig_gpa = get_gpa_distribution_chart()
        st.plotly_chart(fig_gpa, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig_polar = get_course_pass_rate_chart()
        st.plotly_chart(fig_polar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Academic Insight Insights")
        st.write(
            "📊 **Enrollment Insights:** Computer Science represents the largest division, "
            "comprising roughly 40% of the active student base.\n\n"
            "📈 **GPA Target:** The current median GPA stands at **3.8**. "
            "Our Archaeology division, led by Diana Prince, boasts the highest overall cohort average of **4.0**.\n\n"
            "🎯 **Pass Rate Focus:** PHY-102 (Physics) continues to be our most challenging syllabus content, "
            "registering a pass rate threshold of **76%**. System advisors suggest organizing supplemental peer workshops."
        )
        st.markdown('</div>', unsafe_allow_html=True)
