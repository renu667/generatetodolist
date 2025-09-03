import streamlit as st
import requests

# 🔗 Replace with your actual n8n webhook URL
WEBHOOK_URL = "https://renuvaj.app.n8n.cloud/webhook-test/smart_spam_checker"

# 🌟 App Config
st.set_page_config(page_title="Smart Email Spam Checker", layout="centered")
st.title("🧠 Smart Email Spam Detector")
st.caption("Classify incoming emails as **Spam** or **Not Spam** using your AI-powered n8n workflow.")

# 📬 Email Form
with st.form("spam_check_form"):
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("✉️ Email Subject")
    with col2:
        sender = st.text_input("📨 Sender Email")

    body = st.text_area("📝 Email Content", height=180)

    submitted = st.form_submit_button("🚀 Run Spam Check")

# 🧠 Call Webhook on Submit
if submitted:
    if not subject or not sender or not body:
        st.warning("Please fill in all fields.")
    else:
        payload = {
            "subject": subject,
            "sender": sender,
            "body": body
        }

        try:
            response = requests.post(WEBHOOK_URL, json=payload)

            if response.status_code == 200:
                try:
                    result = response.json()

                    classification = result.get("classification", "").strip().lower()
                    reason = result.get("reason", "No reason provided.")

                    if "spam" in classification:
                        st.error("🛑 Classified as: **SPAM**")
                    elif "not spam" in classification:
                        st.success("✅ Classified as: **NOT SPAM**")
                    else:
                        st.info(f"🤖 AI Output: {classification}")

                    with st.expander("📄 AI Explanation"):
                        st.write(reason)

                except Exception as parse_err:
                    st.info("✔️ Response received, but not in expected format.")
                    st.code(response.text)
            elif response.status_code == 404:
                st.error("❌ Webhook not found (404). Check your n8n URL and make sure the workflow is active.")
            else:
                st.error(f"❌ Unexpected error: Status Code {response.status_code}")
        except Exception as e:
            st.error(f"🚫 Request failed: {str(e)}")
