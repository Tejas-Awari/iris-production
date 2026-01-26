from fastapi import FastAPI, HTTPException
import joblib
import os
from .schemas import IrisInput, PredictionOutput

# Initialize the App
app = FastAPI(title="Iris ML API", version="1.0.0")

# Global variable to hold the model
model = None
CLASS_NAMES = {0: "setosa", 1: "versicolor", 2: "virginica"}

@app.on_event("startup")
def load_model():
    """
    Load the model only once when the server starts.
    This prevents reloading heavy files for every request.
    """
    global model
    model_path = "models/model.joblib"
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Did you train it?")
    
    model = joblib.load(model_path)
    print("✅ Model loaded successfully.")

@app.post("/predict", response_model=PredictionOutput)
def predict(data: IrisInput):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Convert input data to list for the model
    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]
    
    # Predict
    prediction = model.predict(features)[0]
    
    return {
        "class_id": int(prediction),
        "class_name": CLASS_NAMES.get(int(prediction), "Unknown")
    }

@app.get("/")
def health_check():
    return {"status": "healthy"}