import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

def build_qa_chain(doc_text: str, api_key: str):
    # Split the document into chunks
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_text(doc_text)

    # Gemini embeddings
    embeddings = GoogleGenerativeAIEmbeddings(google_api_key=api_key, model="models/embedding-001")

    # Create a vectorstore from the text chunks
    db = Chroma.from_texts(texts, embeddings)
    retriever = db.as_retriever()

    # Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key_
