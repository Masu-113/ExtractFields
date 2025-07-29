from fillpdf import fillpdfs

fields = fillpdfs.get_form_fields(
    input_pdf_path=r'C:\Users\msuarez\source\repos\ExtractFields\results2\output_0001.pdf',
    sort=False,
    page_number=None
)

print(fields)

fillpdfs.print_form_fields(input_pdf_path="")