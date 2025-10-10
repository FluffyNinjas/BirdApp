import requests

FASTAPI_URL = "http://localhost:8000/predict"  

def classify_bird(image_file):
    """
    Sends an image to the FastAPI ML service and gets the predicted bird label.
    """
    try:
        files = {"file": image_file}
        response = requests.post(FASTAPI_URL, files=files, timeout=30)
        response.raise_for_status()
        result = response.json()
        return {
            "label": result.get("label"),
            "confidence": result.get("confidence"),
        }
    except requests.RequestException as e:
        print(f"❌ ML service error: {e}")
        return None
