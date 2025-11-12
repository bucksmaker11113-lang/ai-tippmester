import pytesseract
import cv2
import numpy as np
from PIL import Image
import io
import re
import pandas as pd
from datetime import datetime

class VisionAnalyzer:
    def __init__(self, log_path="backend/data/vision_log.csv"):
        self.log_path = log_path

    def analyze_image(self, file_bytes: bytes):
        # Olvasd be a képet byte formátumból
        img_array = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Szürkeárnyalatosítás + előfeldolgozás OCR-hez
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)

        # Tesseract beolvasás
        text = pytesseract.image_to_string(gray, lang="eng")

        # Alap minta felismerés (pl. meccs + odds)
        match = self.extract_match_info(text)
        odds = self.extract_odds(text)

        result = {
            "text_raw": text.strip(),
            "match": match,
            "odds": odds,
            "confidence": 0.8 if match or odds else 0.3,
            "recommendation": self.generate_recommendation(match, odds)
        }

        self._log_result(result)
        return result

    def extract_match_info(self, text: str):
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        for line in lines:
            if "-" in line or "vs" in line.lower():
                return line
        return None

    def extract_odds(self, text: str):
        pattern = re.findall(r"\d+\.\d+", text)
        return [float(x) for x in pattern if 1.01 <= float(x) <= 20.0]

    def generate_recommendation(self, match, odds):
        if not match or not odds:
            return "Nem sikerült meccset vagy oddst felismerni."
        avg_odds = np.mean(odds)
        if avg_odds < 1.8:
            return f"{match}: Alacsony odds ({avg_odds:.2f}), value kevésbé valószínű."
        elif avg_odds < 2.5:
            return f"{match}: Value gyanús ({avg_odds:.2f}) – érdemes figyelni!"
        else:
            return f"{match}: Magas odds ({avg_odds:.2f}) – kockázatos, de potenciális!"

    def _log_result(self, result):
        df = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "match": result.get("match"),
            "odds": result.get("odds"),
            "recommendation": result.get("recommendation"),
        }])
        try:
            df.to_csv(self.log_path, mode="a", header=False, index=False)
        except Exception:
            pass
