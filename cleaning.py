import re
from spellchecker import SpellChecker

def clean_text(text):
    # Remove extra whitespace
    text = re.sub('\s+', ' ', text).strip()
    
    # Correct spelling errors
    spell = SpellChecker()
    words = text.split()
    corrected_words = [spell.correction(word) or word for word in words]
    text = ' '.join(corrected_words)
    
    return text

if __name__ == "__main__":
    from Text_Extraction import extract_text

    # Specify the file name and specific text to search for (if needed)
    filename = "modelcontract-sample.docx"  # Change to the appropriate file path
    specific_text = None  # Provide the specific text if it's an image file

    # Extract text from the specified file
    Extracted_text = extract_text(filename, specific_text)

    # Clean the extracted text
    cleaned_text = clean_text(Extracted_text)

    print(f"Extracted Text: {Extracted_text}")
    print(f"Cleaned Text: {cleaned_text}")
