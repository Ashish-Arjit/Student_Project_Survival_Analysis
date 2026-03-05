import streamlit as st
import pandas as pd
import requests
import backend

st.set_page_config(page_title="Project Survival", layout="wide")

# ROLE AUTHENTICATION
if 'role' not in st.session_state:
    st.session_state.role = None
    st.session_state.student_id = None

if st.session_state.role is None:
    st.title("🔴 Project Failure Risk System")
    st.session_state.role = st.selectbox("👤 Select Your Role", ["student", "teacher"])
    if st.session_state.role == "student":
        st.session_state.student_id = st.text_input("🆔 Your Student/Team ID", value="team_1")
    st.stop()

# SIDEBAR
st.sidebar.title(f"👋 {st.session_state.role.upper()}")
st.sidebar.success(f"Role: {st.session_state.role}")
if st.session_state.role == "student":
    st.sidebar.info(f"Team ID: {st.session_state.student_id}")

st.title("🔴 Project Failure Risk System")
st.info(f"**Logged in as: {st.session_state.role}**")

# CONTROLS
action = st.sidebar.radio("Select Action", ["📊 Create New", "➕ Add Data", "🚀 Train Model", "📈 View Data"])

if action == "📊 Create New":
    st.header("🆕 Create New Dataset")
    if st.button("Create New Dataset", type="primary", use_container_width=True):
        backend.create_new_file()
        st.success("✅ New dataset created!")
        st.rerun()

elif action == "➕ Add Data":
    st.header("➕ Add Project Data")
    
    # STUDENT/TEACHER METRICS
    df = backend.load_data()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("Projects", df['project_id'].nunique())
    col3.metric("Avg Weeks", round(df['week_number'].mean(), 1))
    
    with st.form("entry_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            project_id = st.number_input("Project ID", min_value=1, value=1)
            week_num = st.number_input("Week #", min_value=1, value=1)
            days_worked = st.number_input("Days Worked", 0.0, 7.0, 3)
            lab = st.checkbox("Lab Attended")
        
        with col_b:
            student_id = st.text_input("Student/Team ID", value=st.session_state.student_id or "team_1")
            time_to_event = st.number_input("Expected Fail Week", min_value=1, value=10)
            event = st.radio("Status", [0, 1], format="inline", label_visibility="collapsed")
            st.caption("0=Active, 1=Failed")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            milestones_done = st.number_input("Milestones ✓", 0)
            inactivity = st.number_input("Inactive Streak", 0)
        with col_c2:
            milestones_miss = st.number_input("Milestones ✗", 0)
            days_since_work = st.number_input("Days No Work", 0)
        
        if st.form_submit_button("💾 Save Entry", use_container_width=True):
            data = {
                "project_id": int(project_id), "student_id_or_team_id": student_id,
                "week_number": int(week_num), "days_worked_this_week": int(days_worked),
                "days_since_last_work": int(days_since_work), "lab_attended_this_week": int(lab),
                "milestones_completed_till_week": int(milestones_done),
                "milestones_missed_till_week": int(milestones_miss),
                "inactivity_streak": int(inactivity), "event": int(event),
                "time_to_event": int(time_to_event)
            }
            success, msg = backend.add_entry(data)
            if success:
                st.session_state.student_id = student_id
                st.success("✅ Entry saved!")
                st.rerun()
            else:
                st.error(f"❌ {msg}")

elif action == "🚀 Train Model":
    st.header("🚀 Train Survival Model")
    if st.button("🎯 Train CoxPH Model", type="primary", use_container_width=True):
        with st.spinner("Training model..."):
            summary, msg, success = backend.train_survival_model()
            if success:
                st.success("✅ Model trained successfully!")
                st.dataframe(summary)
                st.download_button("💾 Download Results", summary.to_csv(), "model_summary.csv")
            else:
                st.error(f"❌ {msg}")

elif action == "📈 View Data":
    st.header("📈 Project Dashboard")
    
    # ROLE-BASED DATA FILTERING
    if st.session_state.role == "student":
        student_id = st.session_state.student_id or "team_1"
        st.info(f"Showing YOUR projects (Team: {student_id})")
        response = requests.get(f"http://127.0.0.1:5000/get_projects?student_id={student_id}")
        if response.status_code == 200:
            projects = response.json()['projects']
            st.metric("Your Projects", len(projects))
    else:
        st.info("👨‍🏫 Teacher view: All projects")
    
    # DATA PREVIEW
    response = requests.get(f"http://127.0.0.1:5000/get_data?role={st.session_state.role}")
    if st.session_state.role == "student":
        response = requests.get(f"http://127.0.0.1:5000/get_data?role=student&student_id={st.session_state.student_id}")
    
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        if not df.empty:
            st.dataframe(df.tail(10), use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Records", len(df))
            col2.metric("Your Projects", df['project_id'].nunique())
            col3.metric("Avg Weeks", round(df['week_number'].mean(), 1))
        else:
            st.info("👆 No data yet. Add some entries!")
    else:
        st.error("Backend not running. Start `python app.py`")

# FOOTER
st.markdown("---")
st.caption("🎓 B.Tech CSE Group Project - Survival Analysis for Student Projects")
