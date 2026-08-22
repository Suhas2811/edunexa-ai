from docx import Document


def extract_text_from_docx(file):
    document = Document(file)

    paragraphs = []

    for paragraph_number, paragraph in enumerate(document.paragraphs, start=1):
        text = paragraph.text.strip()

        if text:
            paragraphs.append({
                "paragraph_number": paragraph_number,
                "text": text
            })

    return paragraphs