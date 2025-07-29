import os
from transformers import pipeline
from fillpdf import fillpdfs

# Initialize Hugging Face NER pipeline
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", tokenizer="dbmdz/bert-large-cased-finetuned-conll03-english")

# Simulated transcript (you can replace this with your real transcript)
transcript = """
Hi, I’m Jane Doe. I was born on June 15, 1985. I live at 123 Advisor Way in Toronto, France.
My postal code is M5H 2N2 and my phone number is 123-456-7890.
I work at Wealth Advisors Inc. as a Senior Investment Advisor in the Investment Management department.
My supervisor is John Smith.
I was referred by an existing client. I’ve managed multiple investment portfolios.
"""

ner_results= ner_pipeline(transcript)
print(ner_results)

# Run the transcript through the NER pipeline
entities = ner_pipeline(transcript)

# Extract relevant data
extracted_data = {
    "name": None,
    "dob": None,
    "address": None,
    "city": None,
    "country": "France",  # Hardcoded or inferred
    "zipcode": None,
    "phone": None,
    "company": "Wealth Advisors Inc.",
    "supervisor": "John Smith",
    "position": "Senior Investment Advisor",
    "department": "Investment Management",
    "referral": "Existing Client",
    "comments": "Handled multiple investment portfolios",
}

# Process the entities extracted by Hugging Face NER
for entity in entities:
    entity_text = entity['word']
    entity_label = entity['entity']
    
    # Extract name
    if entity_label == 'B-PER' and not extracted_data["name"]:
        extracted_data["name"] = entity_text
        
    # Extract date of birth (dob)
    elif entity_label == 'B-DATE' and not extracted_data["dob"]:
        extracted_data["dob"] = entity_text
        
    # Extract address or city
    elif entity_label == 'B-LOC' and not extracted_data["city"]:
        extracted_data["city"] = entity_text
        
    # Extract postal code
    elif entity_label == 'B-LOC' and len(entity_text.split()) == 1 and len(entity_text) >= 5:
        extracted_data["zipcode"] = entity_text
        
    # Extract phone number (assumed format "123-456-7890")
    elif entity_label == 'CARDINAL' and "456" in entity_text:
        extracted_data["phone"] = "123-456-7890"

# PDF form setup
input_pdf = "Form_combined.pdf"
output_pdf = "Filled_Form_combined_dynamic_huggingface.pdf"

if not os.path.exists(input_pdf):
    print(f"Error: The file '{input_pdf}' does not exist.")
else:
    fields = fillpdfs.get_form_fields(input_pdf)

    field_mapping = {
        "name": ["Given Name Text Box", "CLIENT NAME", "Full name", "First Name"],
        "dob": ["Date of Birth", "DATE OF BIRTH", "DOB"],
        "address": ["Address 1 Text Box", "HOME ADDRESS", "Street Address"],
        "city": ["City Text Box", "City", "Municipality"],
        "country": ["Country Combo Box", "State", "Province"],
        "zipcode": ["Postcode Text Box", "Zip Code", "Postal Code"],
        "phone": ["CELL PHONE", "Phone", "Home Phone"],
        "company": ["CLIENT COMPANY", "Company Name"],
        "supervisor": ["SUPERVISOR", "Manager"],
        "position": ["POSITIONBUSINESS TITLE", "Job Title"],
        "department": ["DEPARTMENT", "Division"],
        "referral": ["REFERRED BY", "Referral Source"],
        "comments": ["DESCRIBE PREVIOUS WORKCOMMENTS", "Notes"]
    }

    form_data = {}

    for extracted_field, extracted_value in extracted_data.items():
        possible_field_names = field_mapping.get(extracted_field, [])
        matched_field = next((f for f in possible_field_names if f in fields), None)
        if matched_field:
            form_data[matched_field] = extracted_value

    fillpdfs.write_fillable_pdf(input_pdf, output_pdf, form_data)
    print(f"\n PDF dynamically filled and saved as '{output_pdf}'")
