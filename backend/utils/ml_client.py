# backend/utils/ml_client.py
import requests
import os

FASTAPI_URL = os.getenv("ML_SERVICE_URL", "http://localhost:8001/predict")

def classify_bird(image_file):
    """
    Sends an image to the FastAPI ML service for classification.
    Returns: (predicted_label, confidence)
    """
    try:
        files = {"file": (image_file.name, image_file.read(), image_file.content_type)}
        response = requests.post(FASTAPI_URL, files=files, timeout=10)
        response.raise_for_status()
        data = response.json()
        raw_label = data.get("label")
        confidence = data.get("confidence")

        # --- Clean up label: remove number prefix if present ---
        if raw_label and '.' in raw_label:
            raw_label = raw_label.split('.', 1)[1]  # '073.Blue_Jay' → 'Blue_Jay'

        return raw_label, confidence
    except requests.RequestException as e:
        print(f"[ML_CLIENT] Error contacting ML service: {e}")
        return None, None
