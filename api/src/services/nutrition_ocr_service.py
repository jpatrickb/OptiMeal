"""
Nutrition label OCR and parsing service using PaddleOCR.

Extracts text from images and parses key nutrition fields with confidence.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from io import BytesIO
from typing import Dict, Optional

from PIL import Image
import numpy as np

from ..utils.image_processing import preprocess_image

try:
    from paddleocr import PaddleOCR  # type: ignore
except Exception:  # pragma: no cover
    PaddleOCR = None  # type: ignore


@dataclass
class OCRField:
    value: Optional[float]
    confidence: float


class NutritionOCRService:
    """Service for OCR-based extraction of nutrition label data."""

    def __init__(self, lang: str = "en"):
        # Lazy-init OCR model to avoid heavy startup cost
        self.lang = lang
        self._ocr = None

    @property
    def ocr(self):
        if self._ocr is None and PaddleOCR is not None:
            self._ocr = PaddleOCR(use_angle_cls=True, lang=self.lang, show_log=False)
        return self._ocr

    def parse_label(self, image_bytes: bytes) -> Dict[str, OCRField]:
        """Parse nutrition label image and return fields with confidences."""
        processed = preprocess_image(image_bytes)

        text = self._extract_text(processed)
        return self._parse_text(text)

    def _extract_text(self, image_bytes: bytes) -> str:
        if self.ocr is None:
            # Fallback: simple OCR not available; return empty string
            return ""

        # Run OCR
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        result = self.ocr.ocr(np.array(img))

        # Concatenate detected text lines with confidences
        lines = []
        try:
            for page in result:
                for line in page:
                    txt = line[1][0]
                    lines.append(txt)
        except Exception:
            pass
        return "\n".join(lines)

    def _parse_text(self, text: str) -> Dict[str, OCRField]:
        patterns = {
            "calories": r"calories\s*[:\-]?\s*(\d+(?:\.\d+)?)",
            "protein_g": r"protein\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*g",
            "carbs_g": r"(carbohydrate|carb[s]?)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*g",
            "fat_g": r"(total\s+fat|fat)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*g",
        }

        parsed: Dict[str, OCRField] = {
            "calories": OCRField(None, 0.0),
            "protein_g": OCRField(None, 0.0),
            "carbs_g": OCRField(None, 0.0),
            "fat_g": OCRField(None, 0.0),
        }

        lower = text.lower()
        for key, pattern in patterns.items():
            m = re.search(pattern, lower)
            if m:
                # numeric group is last
                try:
                    num_str = m.groups()[-1]
                except Exception:
                    num_str = m.group(1)
                try:
                    parsed[key] = OCRField(float(num_str), 0.8)
                except Exception:
                    parsed[key] = OCRField(None, 0.0)
        return parsed
