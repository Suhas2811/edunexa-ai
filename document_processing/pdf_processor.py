from pypdf import PdfReader


def extract_text_from_pdf(file):
    reader = PdfReader(file)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page_number": page_number,
            "text": text
        })

    return pages