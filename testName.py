import os
from PyPDF2 import PdfReader
from datetime import datetime
import re
from pdftitle import get_title_from_file


def extract_text_from_first_page(pdf_path):
    """Extracts text from the first page of a PDF."""
    reader = PdfReader(pdf_path)
    first_page = reader.pages[0]
    text = first_page.extract_text()
    return text


def generate_keywords(text):
    """Generates a list of keywords from the text. Placeholder for more complex NLP operations."""
    keywords = list(set(re.findall(r"\b\w+\b", text.lower())))
    filtered_keywords = [
        word
        for word in keywords
        if len(word) > 4 and word not in ["the", "and", "with"]
    ]
    return filtered_keywords


def generate_meaningful_name(pdf_path, keywords):
    """Generates a meaningful name based on the PDF content and path."""
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    meaningful_part = "_".join(keywords[:3])
    date_part = datetime.now().strftime("%Y%m%d")
    new_name = f"{base_name}_{meaningful_part}_{date_part}.pdf"
    return new_name


def load_files_and_rename(files):
    """Loads PDF files, analyzes content, and generates meaningful names."""
    renamed_files = []
    for file in files:
        text = extract_text_from_first_page(file["path"])
        keywords = generate_keywords(text)
        new_name = generate_meaningful_name(file["path"], keywords)
        file["new_name"] = new_name
        renamed_files.append(file)
    return renamed_files


files = [
    {
        "name": "koc_holding",
        "path": "assets/files/1667884932282_2202211080817467421.pdf",
    },
    {
        "name": "ramazan_burak",
        "path": "assets/files/RamazanBurakKorkmaz.pdf",
    },
    {
        "name": "yusuf_caliskan",
        "path": "assets/files/Yusuf_Caliskan_Resume.pdf",
    },
]

renamed_files = load_files_and_rename(files)


def extract_title_from_first_page(pdf_path):
    reader = PdfReader(pdf_path)
    print(dir(reader))
    print(reader.metadata)


# tt = extract_title_from_first_page("assets/files/1667884932282_2202211080817467421.pdf")
print(get_title_from_file("assets/files/1667884932282_2202211080817467421.pdf"))
print(get_title_from_file("assets/files/Yusuf_Caliskan_Resume.pdf"))
print(get_title_from_file("assets/files/RamazanBurakKorkmaz.pdf"))
print(get_title_from_file("assets/files/hasan_ozkul.pdf"))
print(get_title_from_file("assets/files/TSLA-Q1-2023-Update.pdf"))
# for file in renamed_files:
#     print(f"Original Name: {file['name']}, New Name: {file['new_name']}")
