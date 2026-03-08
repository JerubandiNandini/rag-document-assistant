# RAG Document Assistant

AI chatbot that answers questions using your documents.

## Features

- Document search using FAISS
- Retrieval Augmented Generation (RAG)
- Streamlit chatbot interface
- Local LLM using Ollama

## Tech Stack

Python
FAISS
SentenceTransformers
Ollama
Streamlit

## Project Architecture

User Question
      ↓
Streamlit UI
      ↓
Vector Search (FAISS)
      ↓
Relevant Documents
      ↓
LLM (Ollama)
      ↓
Answer

## Demo

![RAG Chatbot Demo](screenshots/chatbot_demo.png)

## How to Run

Clone the repository

pip install -r requirements.txt

Create vector database

python code/create_vector_db.py

Run the app

streamlit run code/app.py
