from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
import numpy as np
from PIL import Image
import io
from pathlib import Path
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ML Image Classification API(Pytorch)",
    description="Image classification service using fine-tuned ViT model",
    version="1.0.0"
)

# CORS middleware - allows Django backend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your backend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
processor = None
LABELS = []  
IMG_SIZE = (224, 224)  # Model input size

@app.on_event("startup")
async def load_model():
    """Load the trained model when FastAPI starts"""
    global model, processor, LABELS
    model_dir = Path("models/bird_model")
    try:        
        if not model_dir.exists():
            logger.error(f"Model file not found at {model_dir}")
            logger.info("Please copy your trained model to training/models/bird_model")
            return

        model = AutoModelForImageClassification.from_pretrained(model_dir)
        processor = AutoImageProcessor.from_pretrained(model_dir)
        model.eval()  # Set model to evaluation mode

        LABELS = list(model.config.id2label.values())
        logger.info("✅ Model loaded successfully!")
        logger.info(f"Model input shape: {model.input_shape}")
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        model = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ML Image Classification API",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST with image file)"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if model is not None else "model_not_loaded",
        "model_loaded": model is not None,
        "model_input_shape": str(model.input_shape) if model else None
    }

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Predict the class of an uploaded image
    
    Args:
        file: Image file (jpg, png, etc.)
    
    Returns:
        JSON with prediction label, confidence, and all class probabilities
    """
    
    # Check if model is loaded
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded. Please check server logs."
        )
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail=f"File must be an image. Received: {file.content_type}"
        )
    
    try:
        # Read image file
        contents = await file.read()
        logger.info(f"Received image: {file.filename}, size: {len(contents)} bytes")
        
        # Open and preprocess image
        img = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to model's expected input size
        img = img.resize(IMG_SIZE)
        
        # Process image for model input
        inputs = processor(images=img, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.nn.functional.softmax(logits, dim=1).numpy()[0]
            predicted_index = np.argmax(probs)
            confidence = float(probs[predicted_index])


        predicted_label = model.config.id2label[predicted_index]
        all_predictions = {
            model.config.id2label[i]: float(probs[i]) for i in range(len(probs))
        }
        result = {
            "success": True,
            "label": predicted_label,
            "confidence": confidence,
            "all_predictions": all_predictions,
            "filename": file.filename
        }
        
        logger.info(f"Prediction: {predicted_label} ({confidence:.2%})")
        
        return result
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)