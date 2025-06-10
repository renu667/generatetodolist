# streamlit_todo_gemini.py

import streamlit as st
import datetime
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyANeX9-ytLfkALvYmvIXO80ONZQVfTGiFA")
model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="Smart To-Do List Generator", layout="centered")
st.title("📝 AI-Powered To-Do List Generator")

st.markdown("Fill the task details and click **Generate** to get your personalized To-Do list.")

# Session storage for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Task entry form
with st.form("task_form"):
    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    due_date = st.date_input("Due Date", datetime.date.today())
    due_time = st.time_input("Due Time", datetime.datetime.now().time())
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    status = st.checkbox("Task Completed?")
    recurring = st.checkbox("Recurring Task?")
    frequency = st.selectbox("Recurrence Frequency", ["Daily", "Weekly", "Monthly"]) if recurring else "None"
    reminder = st.time_input("Reminder Time", datetime.time(9, 0))
    
    submitted = st.form_submit_button("➕ Add Task")
    if submitted:
        st.session_state.tasks.append({
            "title": title,
            "description": description,
            "due": f"{due_date} {due_time}",
            "priority": priority,
            "status": "Complete" if status else "Incomplete",
            "recurring": frequency,
            "reminder": str(reminder)
        })
        st.success("Task added successfully!")

# Display tasks
if st.session_state.tasks:
    st.subheader("📋 Task Preview")
    for i, task in enumerate(st.session_state.tasks):
        st.write(f"**{i+1}. {task['title']}**")
        st.write(f"- 📌 Description: {task['description']}")
        st.write(f"- 🗓 Due: {task['due']}")
        st.write(f"- ⏱ Reminder: {task['reminder']}")
        st.write(f"- 🔁 Recurring: {task['recurring']}")
        st.write(f"- 🚦 Priority: {task['priority']}")
        st.write(f"- ✅ Status: {task['status']}")
        st.markdown("---")

# Generate summary with Gemini
if st.button("🔮 Generate AI Summary"):
    prompt_input = "\n".join([f"{t['title']} - {t['description']}, Due: {t['due']}, Priority: {t['priority']}, Status: {t['status']}, Recurring: {t['recurring']}, Reminder: {t['reminder']}" for t in st.session_state.tasks])
    prompt = f"Create a detailed to-do list in bullet points from these tasks:\n{prompt_input}"
    
    with st.spinner("Generating To-Do List..."):
        response = model.generate_content(prompt)
        st.session_state.output = response.text
        st.text_area("🧠 AI-Generated To-Do List", response.text, height=300)

# Download option
if 'output' in st.session_state:
    st.download_button("📥 Download To-Do List", st.session_state.output, "to_do_list.txt")

