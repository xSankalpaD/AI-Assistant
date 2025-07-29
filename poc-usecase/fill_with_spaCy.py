import spacy
from fillpdf import fillpdfs
import re
from datetime import datetime
from audioTranscription import transcribe_audio
from whisperai import whisper_model

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
nlp

# Function to transcribe audio file to text
# transcript= transcribe_audio("./assets/trial1.wav") #google speech recogntion

transcript = whisper_model("./assets/Advisor_Convo.mp3")  # whisperai

# Run spaCy
doc = nlp(transcript)

for ent in doc.ents:
    # print(f"ent.text;ent.label_")
    print(ent.text, ent.label_)

print("done")  # debug line

# Extract entities
extracted_data = {
    "name": None,
    "dob": None,
    "address": None,
    "city": None,
    "country": None,
    "zipcode": None,
    "phone": None,
    "company": None,
    "supervisor": None,
    "position": None,
    "department": None,
    "referral": None,
    "comments": None,
}

# Fill from recognized entities
for ent in doc.ents:
    if ent.label_ == "PERSON" and not extracted_data["name"]:
        extracted_data["name"] = ent.text
        # Split name into given and family names
        parts = ent.text.split()
        extracted_data["given_name"] = parts[0]
        extracted_data["family_name"] = parts[-1] if len(parts) > 1 else ""

    elif ent.label_ == "DATE" and not extracted_data["dob"]:
        extracted_data["dob"] = ent.text

    elif ent.label_ == "GPE":
        if not extracted_data["city"]:
            extracted_data["city"] = ent.text
        elif not extracted_data["country"]:
            extracted_data["country"] = ent.text
    elif ent.label_ == "ORG" and not extracted_data["company"]:
        extracted_data["company"] = ent.text

extracted_data["today"] = datetime.today().strftime("%Y-%m-%d")

print("\nBefore Regex Extraction:")
for field, value in extracted_data.items():
    print(f"{field}: {value}")

# Regex Extraction for Address, Postal Code, Phone
address_match = re.search(
    r"\d{1,5}\s[\w\s]+?(?:Street|St|Avenue|Ave|Road|Rd|Way|Drive|Dr|Boulevard|Blvd)",
    transcript,
    re.IGNORECASE,
)
if address_match:
    extracted_data["address"] = address_match.group(0)

# Postal code - allow lowercase and fix for missing space
postal_match = re.search(r"[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d", transcript)
if postal_match:
    extracted_data["zipcode"] = postal_match.group(0).upper()

# Phone number - allow without dashes
phone_match = re.search(r"\d{10}", transcript)
if phone_match:
    number = phone_match.group(0)
    extracted_data["phone"] = f"{number[:3]}-{number[3:6]}-{number[6:]}"


# Print extracted data for debugging
print("\nExtracted Data:")
for field, value in extracted_data.items():
    print(f"{field}: {value}")

# PDF form setup
input_pdf = "Form_combined.pdf"
output_pdf = "Filled_Form_combined_dynamic.pdf"

fields = fillpdfs.get_form_fields(input_pdf)

field_mapping = {
    "given_name": ["Given Name Text Box", "First Name", "Given Name"],
    "family_name": ["Family Name Text Box", "Last Name", "Surname"],
    "name": ["Full name", "CLIENT NAME"],
    "dob": ["Date of Birth", "DATE OF BIRTH", "DOB"],
    "address": ["Address 1 Text Box", "HOME ADDRESS", "Street Address", "HOME ADDRESS"],
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
    "comments": ["DESCRIBE PREVIOUS WORKCOMMENTS", "Notes"],
    "today": ["Date Completed", "Today’s Date", "Current Date", "DATE"],
}

form_data = {}

for extracted_field, extracted_value in extracted_data.items():
    possible_field_names = field_mapping.get(extracted_field, [])
    matched_field = next((f for f in possible_field_names if f in fields), None)
    if matched_field:
        form_data[matched_field] = extracted_value

fillpdfs.write_fillable_pdf(input_pdf, output_pdf, form_data)
print(f"\n PDF dynamically filled and saved as '{output_pdf}'")
