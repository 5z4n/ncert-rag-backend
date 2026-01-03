from pathlib import Path
from sentence_transformers import SentenceTransformer
import pickle

# ---------------- CONFIG ----------------
PROJECT_ROOT = Path("E:/NCERT_RAG")

CHUNK_DIR = PROJECT_ROOT / "2_chunks"
OUT_DIR = PROJECT_ROOT / "3_embeddings"
OUT_FILE = OUT_DIR / "chunks_embeddings.pkl"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# --------------------------------------

print("🚀 Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

OUT_DIR.mkdir(exist_ok=True)

records = []

print("📂 Reading chunk files...")

for chunk_path in CHUNK_DIR.rglob("*.txt"):
    text = chunk_path.read_text(encoding="utf-8").strip()
    if not text:
        continue

    # -------- METADATA FROM PATH --------
    # Expected path:
    # class_10/science/filename_chunk_12.txt
    rel_parts = chunk_path.relative_to(CHUNK_DIR).parts

    class_name = rel_parts[0].replace("class_", "")
    subject = rel_parts[1]
    filename = rel_parts[-1]

    source = filename.split("_chunk_")[0]
    chunk_id = filename.split("_chunk_")[-1].replace(".txt", "")

    meta = {
        "class": class_name,
        "subject": subject,
        "source": source,
        "chunk_id": chunk_id,
        "path": str(chunk_path)
    }

    records.append({
        "text": text,
        "meta": meta
    })

print(f"✅ Loaded {len(records)} chunks")

# ---------------- EMBEDDINGS ----------------
print("🧠 Generating embeddings...")
embeddings = model.encode(
    [r["text"] for r in records],
    show_progress_bar=True
)

for emb, r in zip(embeddings, records):
    r["embedding"] = emb

# ---------------- SAVE ----------------
with open(OUT_FILE, "wb") as f:
    pickle.dump(records, f)

print("🎉 DONE!")
print(f"📦 Saved embeddings to: {OUT_FILE}")
