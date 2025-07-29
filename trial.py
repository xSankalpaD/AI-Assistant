import spacy
from fillpdf import fillpdfs
import re
from datetime import datetime
from dateutil import parser as dateparser
from whisperai import whisper_model  # Assumes whisper_model(path) returns transcript

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Transcribe using Whisper
transcript = whisper_model("./assets/Advisor_Convo.mp3")  
doc = nlp(transcript)

# --- Extraction Functions ---
def extract_languages(text):
    return re.findall(r"\b(English|French|Mandarin|Spanish|Hindi|Punjabi|Arabic|Urdu)\b", text, re.IGNORECASE)

def extract_gender(text):
    if "female" in text.lower():
        return "Woman"
    if "male" in text.lower():
        return "Man"
    return ""

def extract_fav_color(text):
    match = re.search(r"(go with|favourite colour.*is)\s+(?P<color>\w+)", text, re.IGNORECASE)
    return match.group("color").capitalize() if match else ""

# --- Entity & Regex Extraction ---
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

for ent in doc.ents:
    if ent.label_ == "PERSON" and not extracted_data["name"]:
        extracted_data["name"] = ent.text
        parts = ent.text.strip().split()
        extracted_data["given_name"] = parts[0]
        extracted_data["family_name"] = parts[-1] if len(parts) > 1 else ""

    elif ent.label_ == "DATE" and not extracted_data["dob"]:
        try:
            parsed_date = dateparser.parse(ent.text, fuzzy=True)
            if parsed_date.year < 2020:
                extracted_data["dob"] = parsed_date.strftime("%B %d, %Y")
        except:
            continue

    elif ent.label_ == "GPE":
        if not extracted_data["city"]:
            extracted_data["city"] = ent.text
        elif not extracted_data["country"]:
            extracted_data["country"] = ent.text

    elif ent.label_ == "ORG" and not extracted_data["company"]:
        extracted_data["company"] = ent.text

extracted_data["today"] = datetime.today().strftime("%B %d, %Y")

# Address
address_match = re.search(
    r"\d{1,5}\s[\w\s]+?(?:Street|St|Avenue|Ave|Road|Rd|Way|Drive|Dr|Boulevard|Blvd)",
    transcript, re.IGNORECASE)
if address_match:
    extracted_data["address"] = address_match.group(0)

# Postal code
postal_match = re.search(r"[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d", transcript)
if postal_match:
    extracted_data["zipcode"] = postal_match.group(0).upper()

# Phone number
phone_match = re.search(r"\d{10}", transcript)
if phone_match:
    num = phone_match.group(0)
    extracted_data["phone"] = f"{num[:3]}-{num[3:6]}-{num[6:]}"

# Extra info
extracted_data["gender"] = extract_gender(transcript)
extracted_data["fav_color"] = extract_fav_color(transcript)
extracted_data["languages"] = extract_languages(transcript)

# Job/Referral
for sent in doc.sents:
    line = sent.text.lower()
    if "i’m a" in line or "i am a" in line:
        extracted_data["position"] = sent.text.split("at")[0].split("i’m a")[-1].strip().rstrip(".")
    if "supervisor" in line or "manager" in line:
        match = re.search(r"is (.+)", sent.text, re.IGNORECASE)
        if match:
            extracted_data["supervisor"] = match.group(1).strip().rstrip(".")
    if "department" in line:
        extracted_data["department"] = sent.text.split("in")[-1].strip().rstrip(".")
    if "referred" in line:
        match = re.search(r"referred (?:by|to me by) (?:my|a)?\s*(colleague|friend|advisor)?\s*(.+?)(?:\.|$)", sent.text, re.IGNORECASE)
        if match:
            extracted_data["referral"] = match.group(2).strip()

extracted_data["is_prev_customer"] = "Yes" if "worked with" in transcript.lower() or "another advisor" in transcript.lower() else "No"

# --- PDF Fill ---
pdf_template = "Form_combined.pdf"
output_path = "filled_output.pdf"
form_fields = fillpdfs.get_form_fields(pdf_template)

# Language checkboxes
language_checkboxes = {
    "Language 1 Check Box": "Deutsch",
    "Language 2 Check Box": "English",
    "Language 3 Check Box": "Français",
    "Language 4 Check Box": "Esperanto",
    "Language 5 Check Box": "Latin"
}
language_filled = {key: "Yes" if val.lower() in [lang.lower() for lang in extracted_data["languages"]] else "Off"
                   for key, val in language_checkboxes.items()}

# Normalize values
valid_countries = ['Austria', 'Belgium', 'Britain', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech-Republic',
                   'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland',
                   'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland',
                   'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']
if extracted_data["country"] not in valid_countries:
    print(f"⚠️ '{extracted_data['country']}' not valid for dropdown. Defaulting to 'France'.")
    extracted_data["country"] = "France"

allowed_colors = ["Red", "Blue", "Green", "Yellow", "Black"]
fav_color_normalized = extracted_data["fav_color"] if extracted_data["fav_color"] in allowed_colors else ""

data_dict = {
    "Given Name Text Box": extracted_data.get("given_name", ""),
    "Family Name Text Box": extracted_data.get("family_name", ""),
    "Address 1 Text Box": extracted_data.get("address", ""),
    "Address 2 Text Box": "",
    "City Text Box": extracted_data.get("city", ""),
    "Country Combo Box": extracted_data.get("country", ""),
    "Postcode Text Box": extracted_data.get("zipcode", ""),
    "CELL PHONE": extracted_data.get("phone", ""),
    "HOME PHONE": "",
    "OTHER PHONE": "",
    "DATE OF BIRTH": extracted_data.get("dob", ""),
    "MALEFEMALE": extracted_data.get("gender", ""),
    "REFERRED BY": extracted_data.get("referral", ""),
    "IS THIS A PREVIOUS CUSTOMER": extracted_data.get("is_prev_customer", "No"),
    "POSITIONBUSINESS TITLE": extracted_data.get("position", ""),
    "SUPERVISOR": extracted_data.get("supervisor", ""),
    "WORK ADDRESS": extracted_data.get("company", ""),
    "DEPARTMENT": extracted_data.get("department", ""),
    "CLIENT NAME": extracted_data.get("name", ""),
    "CLIENT COMPANY": extracted_data.get("company", "Luma Ventures"),
    "PROJECTREQUEST OVERVIEW": "Investment portfolio discussion and onboarding",
    "CLIENT ONBOARD INFORMATION": extracted_data.get("phone", ""),
    "HOME ADDRESS": extracted_data.get("address", ""),
    "HOME ADDRESS_2": "",
    "HOME ADDRESS_3": "",
    "WORK ADDRESS_2": "",
    "WORK ADDRESS_3": "",
    "DATE": extracted_data["today"],
    "TENDING ASSOCIATE": "Alex Thompson",
    "Favourite Colour List Box": fav_color_normalized
}
data_dict.update(language_filled)

# Fill unused fields with blanks
for field in form_fields:
    if field not in data_dict:
        data_dict[field] = ""

print("\n Data prepared to fill PDF:")
for key, val in data_dict.items():
    print(f"{key}: {val}")

# Fill PDF
try:
    fillpdfs.write_fillable_pdf(pdf_template, output_path, data_dict)
    print(f"\n PDF saved to: {output_path}")
except Exception as e:
    print(f"\n Failed to fill PDF: {e}")
