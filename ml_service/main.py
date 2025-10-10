from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ML Image Classification API",
    description="Image classification service using pre-trained model",
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
IMG_SIZE = (224, 224)  # Adjust based on your model
LABELS = ['cat', 'dog', 'bird']  # Replace with your actual labels

@app.on_event("startup")
async def load_model():
    """Load the trained model when FastAPI starts"""
    global model
    try:
        model_path = Path("models/image_model.h5")
        
        if not model_path.exists():
            logger.error(f"Model file not found at {model_path}")
            logger.info("Please copy your trained model to fastapi_service/models/image_model.h5")
            return
        
        model = tf.keras.models.load_model(str(model_path))
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
        
        # Convert to array and normalize
        img_array = np.array(img, dtype=np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        logger.info(f"Image preprocessed. Shape: {img_array.shape}")
        
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        
        # Get predicted class and confidence
        predicted_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_idx])
        predicted_label = LABELS[predicted_idx]
        
        # Create response with all class probabilities
        all_predictions = {
            LABELS[i]: float(predictions[0][i]) 
            for i in range(len(LABELS))
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

@app.post("/batch-predict")
async def batch_predict(files: list[UploadFile] = File(...)):
    """
    Predict multiple images at once
    
    Args:
        files: List of image files
    
    Returns:
        List of predictions for each image
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 images per batch"
        )
    
    results = []
    
    for file in files:
        try:
            contents = await file.read()
            img = Image.open(io.BytesIO(contents))
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img = img.resize(IMG_SIZE)
            img_array = np.array(img, dtype=np.float32) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            predictions = model.predict(img_array, verbose=0)
            predicted_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_idx])
            
            results.append({
                "filename": file.filename,
                "label": LABELS[predicted_idx],
                "confidence": confidence
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)