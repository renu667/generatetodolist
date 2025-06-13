import streamlit as st
import requests

# ----------- CONFIGURATION -----------

# Dummy user database
USER_CREDENTIALS = {
    "renu": "renu@1431",
    "sindthu": "sindthu456"
}

# Your n8n webhook URL
N8N_WEBHOOK_URL = "https://vijirenu.app.n8n.cloud/webhook-test/e9a3bf3d-f86b-49ea-94f6-5ed6bf637af3"  # Replace with your actual URL

# ----------- SESSION INITIALIZATION -----------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ----------- LOGIN FUNCTION -----------

def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("Login successful!")
    else:
        st.error("Invalid username or password.")

# ----------- LOGOUT FUNCTION -----------

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully.")

# ----------- MAIN APP -----------

st.set_page_config(page_title="Employee Portal", layout="centered")

st.title("🔐 Secure Employee Portal")

if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(username, password)
else:
    st.subheader(f"Welcome, {st.session_state.username} 👋")
    if st.button("Logout"):
        logout()
        st.stop()

    st.markdown("### 📝 Submit Meeting Action Items")

    with st.form("action_item_form"):
        meeting_date = st.date_input("Meeting Date")
        action_item = st.text_area("Action Item Description")
        assignee = st.text_input("Assigned To")
        due_date = st.date_input("Due Date")
        submit = st.form_submit_button("Submit")

        if submit:
            payload = {
                "username": st.session_state.username,
                "meeting_date": str(meeting_date),
                "action_item": action_item,
                "assignee": assignee,
                "due_date": str(due_date)
            }

            try:
                response = requests.post(N8N_WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.success("Action item submitted successfully ✅")
                else:
                    st.error(f"Failed to submit. Status Code: {response.status_code}")
            except Exception as e:
                st.error(f"Error sending data: {e}")
