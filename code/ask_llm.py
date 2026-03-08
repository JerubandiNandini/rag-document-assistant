import subprocess


def ask_llm(prompt):

    # Run Ollama with Gemma model
    result = subprocess.run(
        ["ollama", "run", "gemma3:4b"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout