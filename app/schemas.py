from pydantic import BaseModel, Field

class PatientInput(BaseModel):
    age: float = Field(..., gt=0, lt=120)
    gender: str
    hypertension: int = Field(..., ge=0, le=1)
    heart_disease: int = Field(..., ge=0, le=1)
    ever_married:str
    residence_type: str
    work_type: str
    avg_glucose_level: float = Field(..., gt=0)
    bmi: float = Field(..., gt=0)
    smoking_status: str
    model_choice: str = 'Baseline'
        
        
class Config:
    json_schema_extra={
        "example":{
            "age" :67.0,
            "gender": "Male",
            "hypertension": 0,
            "heart_disease": 1,
            "ever_married": "Yes" ,
            "residence_type": "Urban",
            "work_type": "Private",
            "avg_glucose_level": 228.69,
            "bmi": 36.6,
            "smoking_status": "formerly smoked" ,
            "model_choice": "Baseline"           
        }
            }
    

class PredictionOutput(BaseModel):
    stroke_probability: float
    risk_label : str