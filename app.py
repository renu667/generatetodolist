import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
import logging

# 🚫 Suppress verbose logs
logging.getLogger("langchain").setLevel(logging.WARNING)

# 🔑 Gemini API Key (Hardcoded — for demo purposes only)
GOOGLE_API_KEY = "AIzaSyAW9AnNsJlJ4p19L4_KQQYelSubrOxOLrM"

# 🧠 Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)

# 🔍 Setup DuckDuckGo Search tool
search_tool = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=search_tool.run,
        description="Use this to search for recent news, real-time facts, or current events."
    )
]

# 🤖 Create the Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# 🎨 Streamlit UI
st.set_page_config(page_title="Gemini Real-Time Q&A 🔍", page_icon="🧠")
st.title("🧠 Real-Time Q&A Assistant 🔍")
st.markdown("Ask me anything about current events, real-world facts, or breaking news! 📢")

# 💬 User Input
query = st.text_input("💬 Enter your question here:", placeholder="e.g., Who won the IPL 2025 final?")

# 🔘 Button to trigger agent
if st.button("🔍 Get Answer"):
    if not query.strip():
        st.warning("⚠️ Please type a question before hitting search.")
    else:
        try:
            with st.spinner("Thinking... 🤔"):
                response = agent.run(query)
            st.success("✅ Here's what I found:")
            st.write(response)
        except Exception as e:
            st.error("❌ Oops! Something went wrong.")
            st.exception(e)

# 👣 Footer
st.markdown("---")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io), [LangChain](https://www.langchain.com), and [Gemini](https://ai.google).")
