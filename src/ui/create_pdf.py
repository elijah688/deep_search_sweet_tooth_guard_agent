from markdown_pdf import MarkdownPdf, Section

def create_pdf(md_text: str) -> str:
    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(md_text))  
    filename = "output.pdf"
    pdf.save(filename)
    return filename
