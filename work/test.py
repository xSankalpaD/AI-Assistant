from fillpdf import fillpdfs

# Load the PDF and inspect fields
input_pdf = "Form_combined.pdf"

# Extract fields from the PDF
fields = fillpdfs.get_form_fields(input_pdf)

# Print out all fields detected in the PDF
print("\n📋 Fields found in the PDF:")
for field, value in fields.items():
    print(f"{field}: {value}")

# If no fields detected, warn user
if not fields:
    print("\n⚠️ No fillable fields detected! Ensure the PDF is interactive.")

