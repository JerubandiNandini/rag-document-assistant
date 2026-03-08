import os

# Absolute path to docs folder
docs_folder = "C:/Users/harik/OneDrive/Desktop/RAG_Project/docs"
documents = []

for filename in os.listdir(docs_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(docs_folder, filename), "r", encoding="utf-8") as f:
            text = f.read()
            documents.append(text)

print(f"Loaded {len(documents)} documents.")