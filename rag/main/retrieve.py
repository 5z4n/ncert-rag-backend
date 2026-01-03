from pathlib import Path
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from rag.main.local_llm import generate_answer  # ✅ ONE correct import

# -------- CONFIG --------
PROJECT_ROOT = Path("E:/NCERT_RAG")

EMBED_FILE = PROJECT_ROOT / "data" / "embeddings" / "chunks_embeddings.pkl"
FAISS_INDEX_FILE = PROJECT_ROOT / "data" / "faiss_index" / "index.faiss"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5
# ------------------------

print("🚀 Loading embedding model...")
embedder = SentenceTransformer(EMBED_MODEL)

print("📦 Loading embeddings + metadata...")
with open(EMBED_FILE, "rb") as f:
    records = pickle.load(f)  # list of dicts

print("📂 Loading FAISS index...")
index = faiss.read_index(str(FAISS_INDEX_FILE))


def retrieve(query, class_name=None, subject=None, top_k=TOP_K):
    query_vec = embedder.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(query_vec)

    _, indices = index.search(query_vec, top_k * 10)

    results = []
    for idx in indices[0]:
        rec = records[idx]

        if class_name and rec["meta"]["class"] != class_name:
            continue
        if subject and rec["meta"]["subject"] != subject:
            continue

        results.append(rec)
        if len(results) >= top_k:
            break

    return results


def answer_from_records(records, question):
    """
    Generates clean answer + minimal NCERT source
    """

    # 🔹 Compact context (NO textbook dump)
    context = "\n".join(r["text"][:400] for r in records[:2])

    answer = generate_answer(context, question)

    meta = records[0]["meta"]
    source = {
        "class": meta.get("class"),
        "subject": meta.get("subject"),
        "file": meta.get("source"),
    }

    return answer, source


# ---------------- CLI TEST ----------------
if __name__ == "__main__":
    query = input("❓ Enter your doubt: ").strip()
    class_name = input("📚 Class (optional): ").strip() or None
    subject = input("📖 Subject (optional): ").strip() or None

    retrieved = retrieve(query, class_name, subject)

    if not retrieved:
        print("\n⚠️ No relevant NCERT content found.")
        exit()

    answer, source = answer_from_records(retrieved, query)

    print("\n🤖 ANSWER:\n")
    print(answer)

    print("\n📘 NCERT SOURCE:")
    print(
        f"Class {source['class']} | "
        f"Subject: {source['subject']} | "
        f"File: {source['file']}"
    )
