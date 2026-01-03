from pathlib import Path
import pickle
import faiss
import numpy as np

# -------- CONFIG --------
PROJECT_ROOT = Path("E:/NCERT_RAG")
EMBED_FILE = PROJECT_ROOT / "3_embeddings" / "chunks_embeddings.pkl"
INDEX_DIR = PROJECT_ROOT / "4_faiss_index"
INDEX_FILE = INDEX_DIR / "index.faiss"
# ------------------------

print("📦 Loading embeddings...")
with open(EMBED_FILE, "rb") as f:
    records = pickle.load(f)

print(f"✅ Loaded {len(records)} embeddings")

# Convert to numpy
embeddings = np.array([r["embedding"] for r in records]).astype("float32")

# Normalize for cosine similarity
faiss.normalize_L2(embeddings)

print("⚙️ Building FAISS index...")
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

INDEX_DIR.mkdir(exist_ok=True)
faiss.write_index(index, str(INDEX_FILE))

print("🎉 Global FAISS index built!")
print(f"📁 Saved at: {INDEX_FILE}")
