import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
import tempfile
import os

def build_qa_chain(doc_text: str, api_key: str):
    # Split text into chunks
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_text(doc_text)

    # Initialize Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        google_api_key=api_key,
        model="models/embedding-001"
    )

    # Create vector DB
    db = Chroma.from_texts(texts, embeddings)
    retriever = db.as_retriever()

    # Initialize Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0
    )

    # Create RetrievalQA Chain
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa

# Streamlit UI
st.set_page_config(page_title="Gemini PDF/Text QA", layout="centered")
st.title("📄 Ask Questions About Your Document (Gemini + LangChain)")

uploaded = st.file_uploader("📤 Upload a .txt or .pdf file", type=["txt", "pdf"])
api_key = st.text_input("🔐 Enter your Gemini API Key", type="password")
question = st.text_input("❓ Ask a question based on the uploaded document")

if st.button("Submit"):
    if not uploaded:
        st.error("Please upload a file.")
    elif not api_key:
        st.error("Please enter your Gemini API key.")
    elif not question:
        st.error("Please enter a question.")
    else:
        # Read uploaded file
        if uploaded.name.endswith(".txt"):
            text = uploaded.read().decode("utf-8")
        else:
            # For PDFs
            try:
                import PyPDF2
                pdf = PyPDF2.PdfReader(uploaded)
                text = "\n\n".join([page.extract_text() or '' for page in pdf.pages])
            except Exception as e:
                st.error("Error reading PDF file.")
                st.stop()

        if not text.strip():
            st.error("No readable text found in the document.")
            st.stop()

        # Build the QA chain
        with st.spinner("Building the QA system..."):
            qa_chain = build_qa_chain(text, api_key)

        # Run the QA
        with st.spinner("Thinking..."):
            try:
                answer = qa_chain.run(question)
                st.success("✅ Answer generated:")
                st.markdown(f"**{answer}**")
            except Exception as e:
                st.error(f"Failed to generate answer: {e}")
