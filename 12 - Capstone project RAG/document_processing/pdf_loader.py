import os
from typing import Tuple, Dict, Optional
from PyPDF2 import PdfReader


def load_pdf(file_path: str) -> Tuple[str, Dict]:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    reader = PdfReader(file_path)
    metadata = reader.metadata

    # Build a list of page texts if extract_text returns a string, otherwise ignore.
    page_texts = []
    for page in reader.pages:
        text: Optional[str] = page.extract_text()
        if text and text.strip():
            page_texts.append(text.strip())

    if not page_texts:
        raise ValueError(f"No text could be extracted from the file {file_path}.")

    # Joining page texts with a newline separator for clarity.
    full_text = "\n".join(page_texts)
    return full_text, metadata