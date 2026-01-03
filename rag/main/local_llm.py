import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "phi3:mini"

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
You are an NCERT school teacher.

Use ONLY the textbook content below.
Answer clearly in simple student language.

Context:
{context}

Question:
{question}

Answer:
"""

    payload = {
    "model": "phi3:mini",
    "messages": [
        {"role": "system", "content": "Answer clearly using NCERT context."},
        {"role": "user", "content": prompt}
    ],
    "stream": False,
    "options": {
        "num_ctx": 2048
    }
}


    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )
        response.raise_for_status()
    except Exception as e:
        return f"Ollama error: {e}"

    data = response.json()
    return data["message"]["content"].strip()
