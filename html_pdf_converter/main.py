"""
The duty of converting HTML to PDF is delegated to an external tool
so this module is just a thin wrapper around it.
"""
import pdfkit
from pathlib import Path

html_file = r"C:\Users\ai\Desktop\smithfu\repositories\lazy-tools\html_pdf_converter\input\2026-03-23-ZAP-Report-localhost.html"
output_file_path = r"C:\Users\ai\Desktop\smithfu\repositories\lazy-tools\html_pdf_converter\output\2026-03-23-ZAP-Report-localhost.pdf"

Path(output_file_path).parent.mkdir(exist_ok=True)

config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Users\ai\Desktop\smithfu\repositories\lazy-tools\html_pdf_converter\tools\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

options = {
    "enable-local-file-access": None,
    "encoding": "UTF-8",
    "page-size": "A4",
}

pdfkit.from_file(
    html_file,
    output_file_path,
    configuration=config,
    options=options
)