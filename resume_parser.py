
from pathlib import Path
from pypdf import PdfReader
from docx import Document


# Function to extract text from a PDF file
def extract_pdf_text(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# Function to extract text from a DOCX file
def extract_docx_text(file_path):

    document = Document(file_path)

    text = ""

    # Extract text from paragraphs
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    # Extract text from tables
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                text += cell.text + " "

            text += "\n"

    return text


# Function to extract text from a TXT file
def extract_txt_text(file_path):

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        text = file.read()

    return text


# Main function to identify the file format
def extract_resume_text(file_path):

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    elif extension == ".txt":
        return extract_txt_text(file_path)

    else:
        raise ValueError("Unsupported file format. Use PDF, DOCX or TXT.")


# Run this program directly to test resume extraction
if __name__ == "__main__":

    resume_path = input("Enter resume file path: ")

    try:
        extracted_text = extract_resume_text(resume_path)

        if extracted_text.strip():
            print("\nResume Text Extracted Successfully!")
            print("-----------------------------------")
            print(extracted_text)
        else:
            print("No readable text found in the resume.")

    except Exception as error:
        print("Error:", error)
