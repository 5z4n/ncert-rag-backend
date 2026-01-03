import importlib

modules = [
    "torch",
    "sentence_transformers",
    "numpy",
    "tqdm",
    "faiss",
    "sklearn",
]

for m in modules:
    try:
        importlib.import_module(m)
        print(f"✅ {m} OK")
    except Exception as e:
        print(f"❌ {m} FAILED → {e}")
