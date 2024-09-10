import os
from Text_Extraction import extract_text
from cleaning import clean_text
from summarize import summarize_cleaned_text

def process_document(filename, specific_text=None):
    if not os.path.exists(filename):
        return "File not found."
    
    extracted_text = extract_text(filename, specific_text)
    cleaned_text = clean_text(extracted_text)
    summary = summarize_cleaned_text(cleaned_text)
    
    return summary

if __name__ == "__main__":
    filename = "modelcontract-sample.docx"  # Update with your file path
    specific_text = None  # Provide specific text if processing an image    
    
    summary = process_document(filename, specific_text)
    print(f"Summary: {summary}")
