import os
import re
from tqdm import tqdm

TEXT_ROOT = r"E:\NCERT_RAG\1_extracted_text"

def clean_text(text: str) -> str:
    # Remove page numbers
    text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

    # Fix hyphenated line breaks
    text = re.sub(r"-\n", "", text)

    # Normalize line breaks
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove junk characters
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", "", text)

    return text.strip()

txt_files = []
for root, _, files in os.walk(TEXT_ROOT):
    for f in files:
        if f.endswith(".txt"):
            txt_files.append(os.path.join(root, f))

print(f"🧹 Cleaning {len(txt_files)} text files (in-place)")

for path in tqdm(txt_files, desc="Cleaning Text"):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    cleaned = clean_text(raw)

    with open(path, "w", encoding="utf-8") as f:
        f.write(cleaned)

print("✅ TEXT CLEANING COMPLETE")
