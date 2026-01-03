import os

TEXT_ROOT = r"E:\NCERT_RAG\1_extracted_text"

bad_files = []

for root, _, files in os.walk(TEXT_ROOT):
    for f in files:
        if not f.endswith(".txt"):
            continue

        path = os.path.join(root, f)
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            text = file.read()

        if len(text.strip()) < 500:
            bad_files.append(path)
        elif text.count(" ") / max(len(text), 1) < 0.05:
            bad_files.append(path)

print(f"🚨 Suspicious files: {len(bad_files)}")

for f in bad_files[:20]:
    print("❌", f)
