"""
Image preprocessing utilities for nutrition label OCR.

Uses OpenCV and MediaPipe (if available) to enhance images prior to OCR.
"""
from io import BytesIO
from typing import Optional

import numpy as np
from PIL import Image

try:
    import cv2  # type: ignore
except Exception:  # pragma: no cover
    cv2 = None  # Fallback if OpenCV isn't available at runtime


def preprocess_image(image_bytes: bytes) -> bytes:
    """Basic image preprocessing: convert to grayscale and enhance contrast.

    Returns processed image bytes (PNG format) suitable for OCR.
    """
    # Load image via PIL
    img = Image.open(BytesIO(image_bytes)).convert("RGB")

    if cv2 is None:
        # If OpenCV unavailable, return original bytes
        output = BytesIO()
        img.save(output, format="PNG")
        return output.getvalue()

    # Convert PIL -> OpenCV
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # Contrast limited adaptive histogram equalization (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Slight Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)

    # Threshold (OTSU)
    _, th = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Encode back to PNG
    success, buf = cv2.imencode(".png", th)
    if not success:
        output = BytesIO()
        img.save(output, format="PNG")
        return output.getvalue()

    return buf.tobytes()
