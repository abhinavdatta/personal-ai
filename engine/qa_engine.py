import ollama
from engine.vector_store import load_store

# Default model
CURRENT_MODEL = "mistral:latest"

db = load_store()


def set_model(name):
    global CURRENT_MODEL
    CURRENT_MODEL = name
    print(f"Switched model to: {CURRENT_MODEL}")


def get_model():
    return CURRENT_MODEL


def answer(question):
    global CURRENT_MODEL

    docs = db.similarity_search(question, k=3)
    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
You are a study assistant.
Answer clearly and accurately.
If unsure, say you don't know.

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model=CURRENT_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
