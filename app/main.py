from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv() # reads .env and makes its values available via os.getenv
    
    
from app.schemas import PatientInput, PredictionOutput  
from app.pipeline import preprocess_and_predict, baseline_model, tuned_model, MODEL_METADATA

ENVIRONMENT = os.getenv("ENVIRONMENT", "development") # second arg is the fallback if .env is missing


app=FastAPI(title= 'Stroke Risk Predictor API')

@app.get("/model-info")
def model_info():
    return MODEL_METADATA
#def read_root():
    # checks the loaded objects actually have a working predict_proba
    # method, not just that they're non-None. a genuine health check,
    # not a static message
    
    #return {"Message": "Stroke Risk Predictor API is running"}
@app.get("/")
def health_check():
    models_ok = hasattr(baseline_model, "predict_proba") and hasattr(tuned_model,"predict_proba")
    return {
        "status": "healthy" if models_ok else "degraded",
        "model_loaded": models_ok,
        "environment": ENVIRONMENT
    }
    

@app.post("/predict", response_model= PredictionOutput)
def predict(patient: PatientInput):
    probability = preprocess_and_predict(patient)
    risk_label = 'Higher Risk' if probability>=0.5 else 'Lower Risk'
    return PredictionOutput(stroke_probability = probability, risk_label = risk_label)

