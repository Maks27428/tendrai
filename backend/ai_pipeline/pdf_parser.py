import fitz


def parse_pdf(file_path: str) -> dict:
    """Extract text from PDF using PyMuPDF, preserving structure."""
    doc = fitz.open(file_path)
    pages = []
    full_text_parts = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        pages.append({
            'page': page_num + 1,
            'text': text,
        })
        full_text_parts.append(f"--- Страница {page_num + 1} ---\n{text}")

    doc.close()

    full_text = "\n\n".join(full_text_parts)

    # Truncate to ~150K chars to stay within Claude's context window
    if len(full_text) > 150000:
        full_text = full_text[:150000] + "\n\n[... документ обрезан из-за большого объёма ...]"

    return {
        'full_text': full_text,
        'page_count': len(pages),
        'pages': pages,
    }
