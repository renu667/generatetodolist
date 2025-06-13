import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader

st.set_page_config(page_title="PDF RAG Demo", layout="centered")

st.title("📄 PDF Loader using LangChain")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    with open("temp_uploaded.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded and saved successfully!")

    # Load PDF content using LangChain PyPDFLoader
    try:
        loader = PyPDFLoader("temp_uploaded.pdf")
        documents = loader.load()

        st.subheader("📄 Extracted Document Content")
        for i, doc in enumerate(documents):
            st.markdown(f"**Page {i+1}:**")
            st.write(doc.page_content)

    except Exception as e:
        st.error(f"❌ Error loading PDF: {e}")

    # Optional: Cleanup file
    os.remove("temp_uploaded.pdf")
