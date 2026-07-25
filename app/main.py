from fastapi import FastAPI
from app.schemas import PatientInput, PredictionOutput  
from app.pipeline import preprocess_and_predict

app=FastAPI(title= 'Stroke Risk Predictor API')

@app.get("/")
def read_root():
    return {"Message": "Stroke Risk Predictor API is running"}

@app.post("/predict", response_model= PredictionOutput)
def predict(patient: PatientInput):
    probability = preprocess_and_predict(patient)
    risk_label = 'Higher Risk' if probability>=0.5 else 'Lower Risk'
    return PredictionOutput(stroke_probability = probability, risk_label = risk_label)
