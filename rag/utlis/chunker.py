import os
from tqdm import tqdm

# =========================
# PATH CONFIG
# =========================
BASE_DIR = r"E:\NCERT_RAG"
TEXT_ROOT = os.path.join(BASE_DIR, "1_extracted_text")
CHUNK_ROOT = os.path.join(BASE_DIR, "2_chunks")

CHUNK_SIZE = 500      # words per chunk
OVERLAP = 80          # overlapping words

# =========================
# HELPERS
# =========================
def chunk_text(words, chunk_size, overlap):
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start += chunk_size - overlap

    return chunks

def mirror_chunk_path(txt_path):
    """
    1_extracted_text/class_6/english/file.txt
    ->
    2_chunks/class_6/english/file_chunk_000.txt
    """
    relative = os.path.relpath(txt_path, TEXT_ROOT)
    base, _ = os.path.splitext(relative)
    return os.path.join(CHUNK_ROOT, base)

# =========================
# MAIN
# =========================
def run_chunking():
    txt_files = []

    for root, _, files in os.walk(TEXT_ROOT):
        for f in files:
            if f.lower().endswith(".txt"):
                txt_files.append(os.path.join(root, f))

    print(f"📄 Text files found: {len(txt_files)}")

    for txt_path in tqdm(txt_files, desc="Chunking Text"):
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            continue

        words = text.split()
        chunks = chunk_text(words, CHUNK_SIZE, OVERLAP)

        chunk_base_dir = mirror_chunk_path(txt_path)
        os.makedirs(chunk_base_dir, exist_ok=True)

        for i, chunk in enumerate(chunks):
            chunk_file = os.path.join(
                chunk_base_dir,
                f"chunk_{i:03d}.txt"
            )
            with open(chunk_file, "w", encoding="utf-8") as cf:
                cf.write(chunk)

    print("✅ CHUNKING COMPLETE")

if __name__ == "__main__":
    run_chunking()
