import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

# ✅ Set your Gemini API Key
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyAW9AnNsJlJ4p19L4_KQQYelSubrOxOLrM"  # Replace this

# ✅ Initialize Gemini model via LangChain
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

# ✅ Define the prompt template
prompt = ChatPromptTemplate.from_template(
    "Translate the following English sentence to French:\n\n{english_text}"
)

# ✅ Streamlit UI
st.set_page_config(page_title="English to French Translator", layout="centered")
st.title("🌍 English to French Translator")

user_input = st.text_input("Enter an English sentence:")

if user_input:
    chain = prompt | llm  # LangChain chaining method
    response = chain.invoke({"english_text": user_input})
    st.success("Translated to French:")
    st.write(response.content)
