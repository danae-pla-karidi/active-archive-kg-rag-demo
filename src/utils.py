
"""Utility helpers: PDF parsing, logging config."""

import logging, pathlib
import fitz  # PyMuPDF

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='[%(asctime)s] %(levelname)s:%(name)s: %(message)s',
        datefmt='%H:%M:%S'
    )

def parse_pdf(pdf_path: str) -> str:
    """Extract text from PDF using PyMuPDF (fitz)."""
    doc = fitz.open(pdf_path)
    texts = []
    for page in doc:
        texts.append(page.get_text())
    return '\n'.join(texts)
