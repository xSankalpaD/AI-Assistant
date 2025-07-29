from fillpdf import fillpdfs

# Input and output PDFs
input_pdf = "Form_combined.pdf"
output_pdf = "Filled_Form_combined_dynamic.pdf"

# Extract fields from the PDF
fields = fillpdfs.get_form_fields(input_pdf)

# Print out all detected fields (debugging)
#print("\n📋 Fields found in the PDF:")
#for field in fields.keys():
#    print(field)

# Define flexible field mappings to normalize different PDF structures
field_mapping = {
    "name": ["Given Name Text Box", "CLIENT NAME", "Full name", "First Name"],
    "dob": ["Date of Birth", "DATE OF BIRTH", "DOB"],
    "address": ["Address 1 Text Box", "HOME ADDRESS", "Street Address"],
    "city": ["City Text Box", "City", "Municipality"],
    "country": ["Country Combo Box", "State", "Province"],
    "zipcode": ["Postcode Text Box", "Zip Code", "Postal Code"],
    "phone": ["CELL PHONE", "Phone", "Home Phone"],
    "gender": ["Gender List Box", "MALEFEMALE"],
    "company": ["CLIENT COMPANY", "Company Name"],
    "supervisor": ["SUPERVISOR", "Manager"],
    "position": ["POSITIONBUSINESS TITLE", "Job Title"],
    "department": ["DEPARTMENT", "Division"],
    "referral": ["REFERRED BY", "Referral Source"],
    "comments": ["DESCRIBE PREVIOUS WORKCOMMENTS", "Notes"]
}

# Example extracted data (simulated)
extracted_data = {
    "name": "Jane Doe",
    "dob": "1985-06-15",
    "address": "123 Advisor Way, Toronto, ON",
    "city": "Toronto",
    "country": "France",  # FIXED: Changed from "Ontario" to "France"
    "zipcode": "M5H 2N2",
    "phone": "123-456-7890",
    "gender": "Woman",  # FIXED: Changed from "Female" to "Woman"
    "company": "Wealth Advisors Inc.",
    "supervisor": "John Smith",
    "position": "Senior Investment Advisor",
    "department": "Investment Management",
    "referral": "Existing Client",
    "comments": "Handled multiple investment portfolios"
}

# Dynamically map extracted data to actual PDF fields
form_data = {}

for extracted_field, extracted_value in extracted_data.items():
    possible_field_names = field_mapping.get(extracted_field, [])

    # Find the first field name that exists in the actual PDF fields
    matched_field = None
    for possible_field in possible_field_names:
        if possible_field in fields:
            matched_field = possible_field
            break

    if matched_field:
        form_data[matched_field] = extracted_value

# Fill the form dynamically
fillpdfs.write_fillable_pdf(input_pdf, output_pdf, form_data)

print(f"\n✅ PDF dynamically filled and saved as '{output_pdf}'")
