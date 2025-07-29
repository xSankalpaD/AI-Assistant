from fillpdf import fillpdfs

# Paths to input and output PDFs
input_pdf = "Form.pdf"
output_pdf = "filled_client_intake.pdf"

# Extract fields from the PDF
fields = fillpdfs.get_form_fields(input_pdf)
print("\n📋 Fields found in the PDF:")
for field, value in fields.items():
    print(f"{field}: {value}")

# Sample data to fill in (ensure these match field names from the PDF)
form_data = {
    "DATE": "2024-03-13",
    "TENDING ASSOCIATE": "John Doe",
    "CLIENT NAME": "Jane Smith",
    "CLIENT COMPANY": "Acme Corp",
    "PROJECTREQUEST OVERVIEW": "New client onboarding.",
    "HOME ADDRESS": "123 Main St",
    "CELL PHONE": "123-456-7890",
    "OTHER PHONE": "987-654-3210",
    "POSITIONBUSINESS TITLE": "Senior Advisor",
    "SUPERVISOR": "Michael Johnson",
    "WORK ADDRESS": "456 Business St",
    "DEPARTMENT": "Wealth Management",
    "DATE OF BIRTH": "1985-06-15",
    "MALEFEMALE": "Female",
    "IS THIS A PREVIOUS CUSTOMER": "Yes",
    "REFERRED BY": "Online Inquiry",
    "DESCRIBE PREVIOUS WORKCOMMENTS": "Worked on prior investment plans."
}

# Fill the PDF with provided data
fillpdfs.write_fillable_pdf(input_pdf, output_pdf, form_data)

print(f"\n✅ PDF filled successfully and saved as '{output_pdf}'")
