import spacy
from spacy.pipeline import EntityRuler
import re
import json

# Load model and add custom EntityRuler
nlp = spacy.load("en_core_web_sm")
ruler = EntityRuler(nlp, overwrite_ents=True)
patterns = [
    {"label": "POSITION", "pattern": "Senior Investment Advisor"},
    {"label": "DEPARTMENT", "pattern": "Investment Management"},
    {"label": "COMPANY", "pattern": "Wealth Advisors Inc."},
    {"label": "SUPERVISOR", "pattern": "John Smith"},
    {"label": "PHONE", "pattern": [{"TEXT": {"REGEX": r"\d{3}-\d{3}-\d{4}"}}]},
]
ruler.add_patterns(patterns)
nlp.add_pipe(ruler, before="ner")

# Load transcript
with open("transcript.txt", "r") as file:
    transcript = file.read()

doc = nlp(transcript)

# Extracted values
extracted_data = {
    "name": None,
    "dob": None,
    "address": None,
    "city": None,
    "country": "France",
    "zipcode": None,
    "phone": None,
    "gender": "Woman",
    "company": None,
    "supervisor": None,
    "position": None,
    "department": None,
    "referral": "Existing Client",
    "comments": "Handled multiple investment portfolios"
}

# Extract using NER
for ent in doc.ents:
    if ent.label_ == "PERSON" and not extracted_data["name"]:
        extracted_data["name"] = ent.text
    elif ent.label_ == "DATE" and not extracted_data["dob"]:
        extracted_data["dob"] = ent.text
    elif ent.label_ == "GPE" and not extracted_data["city"]:
        extracted_data["city"] = ent.text
    elif ent.label_ == "ORG" and not extracted_data["company"]:
        extracted_data["company"] = ent.text
    elif ent.label_ == "POSITION" and not extracted_data["position"]:
        extracted_data["position"] = ent.text
    elif ent.label_ == "DEPARTMENT" and not extracted_data["department"]:
        extracted_data["department"] = ent.text
    elif ent.label_ == "SUPERVISOR" and not extracted_data["supervisor"]:
        extracted_data["supervisor"] = ent.text
    elif ent.label_ == "PHONE" and not extracted_data["phone"]:
        extracted_data["phone"] = ent.text

# Regex backup for phone number
if not extracted_data["phone"]:
    match = re.search(r"\d{3}-\d{3}-\d{4}", transcript)
    if match:
        extracted_data["phone"] = match.group()

# Regex for address (very basic for demo)
if not extracted_data["address"]:
    match = re.search(r"\d{2,5}\s\w+\s(?:Street|St|Avenue|Ave|Way|Road|Rd)", transcript)
    if match:
        extracted_data["address"] = match.group()

# Zip code
if not extracted_data["zipcode"]:
    match = re.search(r"[A-Z]\d[A-Z]\s?\d[A-Z]\d", transcript)
    if match:
        extracted_data["zipcode"] = match.group()

# Save results
with open("extracted_data.json", "w") as f:
    json.dump(extracted_data, f, indent=2)

print("✅ Extracted enhanced data saved to extracted_data.json")
