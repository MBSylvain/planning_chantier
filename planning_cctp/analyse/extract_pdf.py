# Extraction de texte PDF (natif + OCR)

import pdfplumber
import pytesseract
from PIL import Image
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
	"""Extrait le texte d'un PDF (natif, sans OCR)."""
	import pdfplumber
	import io
	text = ""
	with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
		for page in pdf.pages:
			text += page.extract_text() or ""
			text += "\n"
	return text
