import sys
import cv2
import numpy as np
from PIL import Image
import pytesseract
import os
import re

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    try:
        # Read the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise and improve thresholding
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Apply morphological operations to clean up the image
        kernel = np.ones((1, 1), np.uint8)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Resize the image to double its original size
        resized = cv2.resize(morph, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        # Save the preprocessed image to a temporary file
        temp_filename = "temp_image.png"
        cv2.imwrite(temp_filename, resized)

        return temp_filename
    except Exception as e:
        print(f"Error in preprocessing image: {e}")
        return None

def extract_text_from_image(image_path, specific_text):
    try:
        # Preprocess the image
        preprocessed_image_path = preprocess_image(image_path)
        if preprocessed_image_path is None:
            return "Preprocessing failed."

        # Open the preprocessed image with PIL
        img = Image.open(preprocessed_image_path)

        # Perform OCR using Tesseract
        text = pytesseract.image_to_string(img, lang='eng', config='--psm 6 --oem 3')

        # Print the extracted text for debugging
        print("Extracted Text:\n", text)

        # Clean up the temporary file
        os.remove(preprocessed_image_path)

        # Search for the specific text using regular expressions
        if re.search(re.escape(specific_text), text, re.IGNORECASE):
            return f"Found '{specific_text}' in the image."
        else:
            return f"'{specific_text}' not found in the image."
    except Exception as e:
        print(f"Error in extracting text from image: {e}")
        return "Extraction failed."

if __name__ == "__main__":
    # Read command line arguments for file location and text to search
    if len(sys.argv) < 2:
        print("Usage: python Text_Extraction_img.py <image_file_path> <specific_text>")
        sys.exit(1)

    image_file_location = sys.argv[1]
    text_to_search = sys.argv[2] if len(sys.argv) > 2 else ""

    if not os.path.exists(image_file_location):
        print(f"File not found: {image_file_location}")
    else:
        result = extract_text_from_image(image_file_location, text_to_search)
        print(result)
