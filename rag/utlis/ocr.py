import os
from pdf2image import convert_from_path
import pytesseract
from tqdm import tqdm

# =========================
# PATH CONFIG
# =========================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\Users\faizan\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin"

BASE_DIR = r"E:\NCERT_RAG"
PDF_ROOT = os.path.join(BASE_DIR, "0_raw_pdfs")
TEXT_ROOT = os.path.join(BASE_DIR, "1_extracted_text")

os.makedirs(TEXT_ROOT, exist_ok=True)

# =========================
# FUNCTIONS
# =========================
def pdf_to_text(pdf_path):
    """OCR a single PDF and return extracted text"""
    text = []

    try:
        pages = convert_from_path(
            pdf_path,
            dpi=300,
            poppler_path=POPPLER_PATH
        )

        for page in pages:
            text.append(
                pytesseract.image_to_string(page, lang="eng")
            )

    except Exception as e:
        print(f"❌ Failed OCR: {pdf_path} | {e}")

    return "\n".join(text)


def mirror_output_path(pdf_path):
    """
    0_raw_pdfs/class_6/english/fepr101.pdf
    ->
    1_extracted_text/class_6/english/fepr101.txt
    """
    relative = os.path.relpath(pdf_path, PDF_ROOT)
    relative = os.path.splitext(relative)[0] + ".txt"
    return os.path.join(TEXT_ROOT, relative)


def delete_empty_txt_files():
    deleted = 0

    for root, _, files in os.walk(TEXT_ROOT):
        for f in files:
            if f.lower().endswith(".txt"):
                path = os.path.join(root, f)
                if os.path.getsize(path) == 0:
                    os.remove(path)
                    deleted += 1

    print(f"🧹 Deleted {deleted} empty .txt files")


def run_ocr():
    # STEP 0: clean empty txt files
    delete_empty_txt_files()

    pdf_files = []

    for root, _, files in os.walk(PDF_ROOT):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, f))

    print(f"📄 Total PDFs found: {len(pdf_files)}")

    for pdf_path in tqdm(pdf_files, desc="OCR Processing"):
        out_txt = mirror_output_path(pdf_path)

        # Skip ONLY if txt exists AND is non-empty
        if os.path.exists(out_txt):
            with open(out_txt, "r", encoding="utf-8", errors="ignore") as f:
                if f.read().strip():
                    continue

        os.makedirs(os.path.dirname(out_txt), exist_ok=True)

        text = pdf_to_text(pdf_path)

        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(text)


if __name__ == "__main__":
    run_ocr()
    print("✅ OCR COMPLETE")