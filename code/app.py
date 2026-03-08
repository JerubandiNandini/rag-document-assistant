import streamlit as st
from rag_pipeline import search, ask_llm

st.set_page_config(
    page_title="RAG AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 RAG AI Chatbot")
st.write("Ask questions from your document knowledge base.")

# User input
query = st.text_input("Enter your question:")

if query:

    # Retrieve relevant documents
    docs = search(query)

    # Combine retrieved text for prompt
    context = "\n\n".join([doc["text"] for doc in docs])

    prompt = f"""
You are an AI assistant. Answer the question using the context below.

Context:
{context}

Question:
{query}

Answer:
"""

    # Ask LLM
    answer = ask_llm(prompt)

    st.subheader("🤖 Answer")
    st.write(answer)

    st.subheader("📚 Sources")
    for doc in docs:
        st.write(f"- {doc['source']}")