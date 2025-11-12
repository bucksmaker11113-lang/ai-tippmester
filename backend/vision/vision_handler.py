"""
Vision Handler – Tippmester 5.2
Kép alapú meccs felismerés (OCR + AI interpretáció).
"""

import pytesseract
import cv2
import re
from .context_builder import VisionContextBuilder

class VisionHandler:
    def __init__(self):
        self.builder = VisionContextBuilder()

    def analyze_image(self, image_path: str):
        """Kép elemzése, csapatnevek és oddsok felismerése."""
        try:
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            context = self.builder.extract_context(text)
            return {"status": "ok", "context": context}
        except Exception as e:
            return {"status": "error", "detail": str(e)}
