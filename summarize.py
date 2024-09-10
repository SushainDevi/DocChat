import re
from transformers import T5ForConditionalGeneration, T5Tokenizer
from concurrent.futures import ThreadPoolExecutor
from cleaning import clean_text

# Initialize the T5 model and tokenizer
model_name = "t5-small"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def extract_key_details(text):
    details = {}
    
    # Extract production company details
    company_match = re.search(r'Production Company:\s*(.+)', text)
    if company_match:
        details['Production Company'] = company_match.group(1).strip()
    else:
        details['Production Company'] = "Not found"

    # Extract director details
    director_match = re.search(r'Director:\s*(.+)', text)
    if director_match:
        details['Director'] = director_match.group(1).strip()
    else:
        details['Director'] = "Not found"

    # Extract phone numbers
    phone_matches = re.findall(r'\(\d{3}\) \d{3}-\d{4}', text)
    details['Phone Numbers'] = phone_matches if phone_matches else ["Not found"]

    # Extract email addresses
    email_matches = re.findall(r'\S+@\S+', text)
    details['Email Addresses'] = email_matches if email_matches else ["Not found"]

    # Extract addresses (very basic pattern matching)
    address_matches = re.findall(r'\d{3,}\s\w+\s\w+[,]\s\w+\s\w+\s\d{5}', text)
    details['Addresses'] = address_matches if address_matches else ["Not found"]

    return details

def abstractive_summary(text, max_length=300, min_length=80):
    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def split_text(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_chunk(chunk):
    return abstractive_summary(chunk)

def summarize_cleaned_text(cleaned_text):
    text_parts = split_text(cleaned_text, chunk_size=1000)
    full_summary = ""

    with ThreadPoolExecutor() as executor:
        summaries = list(executor.map(summarize_chunk, text_parts))

    full_summary = " ".join(summaries)
    return full_summary.strip()

def create_structured_summary(cleaned_text, full_summary):
    key_details = extract_key_details(cleaned_text)
    structured_summary = f"""
    Production Company: {key_details['Production Company']}
    Director: {key_details['Director']}
    Phone Numbers: {", ".join(key_details['Phone Numbers'])}
    Email Addresses: {", ".join(key_details['Email Addresses'])}
    Addresses: {", ".join(key_details['Addresses'])}

    Summary:
    {full_summary}
    """
    return structured_summary

if __name__ == "__main__":
    from Text_Extraction import extract_text

    filename = "modelcontract-sample.docx"
    specific_text = None

    extracted_text = extract_text(filename, specific_text)
    cleaned_text = clean_text(extracted_text)
    summary = summarize_cleaned_text(cleaned_text)
    structured_summary = create_structured_summary(cleaned_text, summary)

    print(f"Structured Summary:\n{structured_summary}")
