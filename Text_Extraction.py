import os
import pandas as pd
import subprocess
import PyPDF2
import docx

def extract_text_from_pdf(file):
    try:
        pdfReader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdfReader.pages:
            text += page.extract_text() or ''
        return text
    except Exception as e:
        print(f"Error in extracting text from PDF: {e}")
        return "Extraction failed."

def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        full_text = [para.text for para in doc.paragraphs]
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error in extracting text from DOCX: {e}")
        return "Extraction failed."

def extract_text_from_image(filename):
    try:
        result = subprocess.run(
            ['python', 'Text_Extraction_img.py', filename],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error in extracting text from image: {e}")
        return "Extraction failed."

def extract_text(file):
    try:
        file_type = os.path.splitext(file.name)[1].upper()

        if file_type == '.PDF':
            return extract_text_from_pdf(file)

        elif file_type == '.DOCX':
            return extract_text_from_docx(file)

        elif file_type == '.TXT':
            return file.read().decode("utf-8")

        elif file_type == '.XLSX':
            df = pd.read_excel(file)
            return df.to_string()

        elif file_type in ['.JPG', '.JPEG', '.PNG']:
            return extract_text_from_image(file)

        else:
            return "Unsupported file type."
    except Exception as e:
        print(f"Error in extracting text: {e}")
        return "Extraction failed."