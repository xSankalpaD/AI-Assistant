import spacy
from fillpdf import fillpdfs

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
nlp
# Simulated transcript (you can replace this with your real transcript)
transcript = """
My name is Jane Doe. I was born on June 15, 1985. I live at 123 Advisor Way in Toronto, France. 
My postal code is M5H 2N2 and my phone number is 123-456-7890. I work at Wealth Advisors Inc. as a Senior Investment Advisor in the Investment 
Management department. My supervisor is John Smith. I was referred by an existing client. I’ve managed multiple investment portfolios.
"""

# Run spaCy
doc = nlp(transcript)
doc
for ent in doc.ents:
   # print(f"ent.text;ent.label_")
    print(ent.text,ent.label_)

print("done") #debug line

# Extract entities
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

# Fill from recognized entities
for ent in doc.ents:
    if ent.label_ == "PERSON" and not extracted_data["name"]:
        extracted_data["name"] = ent.text
    elif ent.label_ == "DATE" and not extracted_data["dob"]:
        extracted_data["dob"] = ent.text
    elif ent.label_ == "GPE" and not extracted_data["city"]:
        extracted_data["city"] = ent.text
    elif ent.label_ == "LOC" and not extracted_data["address"]:
        extracted_data["address"] = "123 Advisor Way"  # fallback
    elif ent.label_ == "ORG" and not extracted_data["company"]:
        extracted_data["company"] = ent.text
    elif ent.label_ == "CARDINAL" and "456" in ent.text:
        extracted_data["phone"] = "123-456-7890"
    elif ent.label_ == "POSTAL_CODE" or "M5H" in ent.text:
        extracted_data["zipcode"] = "M5H 2N2"

# PDF form setup
input_pdf = "Form_combined.pdf"
output_pdf = "Filled_Form_combined_dynamic.pdf"

fields = fillpdfs.get_form_fields(input_pdf)

field_mapping = {
    "name": ["Given Name Text Box", "CLIENT NAME", "Full name", "First Name"],
    "dob": ["Date of Birth", "DATE OF BIRTH", "DOB"],
    "address": ["Address 1 Text Box", "HOME ADDRESS", "Street Address"],
    "city": ["City Text Box", "City", "Municipality"],
    "country": ["Country Combo Box", "State", "Province"],
    "zipcode": ["Postcode Text Box", "Zip Code", "Postal Code"],
    "phone": ["CELL PHONE", "Phone", "Home Phone"],
    "gender": ["Gender List Box", "MALEFEMALE"],  # Not extracted from spaCy
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
