import pdfplumber
from docx import Document

def parse_resume(file_path):

    text = ""

    if file_path.endswith(".pdf"):

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                content = page.extract_text()

                if content:
                    text += content

    elif file_path.endswith(".docx"):

        doc = Document(file_path)

        for p in doc.paragraphs:
            text += p.text + "\n"

    return text