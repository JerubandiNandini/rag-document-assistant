import os

# Absolute path to docs folder
docs_folder = "___our specified doc foler path should be entioned here___"
documents = []

for filename in os.listdir(docs_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(docs_folder, filename), "r", encoding="utf-8") as f:
            text = f.read()
            documents.append(text)

print(f"Loaded {len(documents)} documents.")
