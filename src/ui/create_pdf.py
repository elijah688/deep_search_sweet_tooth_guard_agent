import markdown2
from weasyprint import HTML

def create_pdf(md_text: str, output_file="output.pdf"):
    html_text = markdown2.markdown(md_text)  # Markdown → HTML
    HTML(string=html_text).write_pdf(output_file)
    return output_file
