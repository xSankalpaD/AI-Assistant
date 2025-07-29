from fillpdf import fillpdfs

# Paths to input and output PDFs
input_pdf = "fillable_form.pdf"
output_pdf = "filled_form.pdf"

# Print available fields (for debugging & understanding field names)
fields = fillpdfs.get_form_fields(input_pdf)
print("\n📋 Fields found in the PDF:")
for field, value in fields.items():
    print(f"{field}: {value}")

# Sample data to fill in (matches fields from the PDF)
form_data = {
    "Given Name Text Box": "Jane",
    "Family Name Text Box": "Doe",
    "Address 1 Text Box": "123 Advisor Way",
    "House nr Text Box": "Suite 400",
    "Postcode Text Box": "M5H 2N2",
    "City Text Box": "Toronto",
    "Country Combo Box": "France",  # Changed to match allowed options
    "Gender List Box": "Woman",
    "Height Formatted Field": "165",
    "Driving License Check Box": "Yes",
    "Language 1 Check Box": "Yes",  # Deutsch
    "Language 2 Check Box": "Yes",  # English
    "Language 3 Check Box": "No",
    "Language 4 Check Box": "No",
    "Language 5 Check Box": "No",
    "Favourite Colour List Box": "Blue"
}

# Fill the form
fillpdfs.write_fillable_pdf(input_pdf, output_pdf, form_data)

print(f"\n PDF filled successfully and saved as '{output_pdf}'")
