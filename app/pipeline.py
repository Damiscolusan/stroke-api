from pathlib import Path
import pandas as pd
import joblib   

# __file__ is pipeline.py's own real location on disk, always, no matter
# where the terminal is sitting when uvicorn starts. .parent steps up one
# folder (from app/ to stroke_app/), giving a reliable anchor point.

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR/ "model"

baseline_model = joblib.load(MODEL_DIR / 'stroke_model_baseline.pkl')
tuned_model = joblib.load(MODEL_DIR / 'stroke_model_tuned.pkl')
scaler = joblib.load(MODEL_DIR / 'stroke_scaler.pkl')
feature_columns = joblib.load(MODEL_DIR / 'stroke_feature_columns.pkl')
encoding_maps = joblib.load(MODEL_DIR / 'stroke_encoding_maps.pkl')

def preprocess_and_predict(patient):
    input_dict = {
        'gender':encoding_maps['gender'][patient.gender],
        'age':patient.age,
        'hypertension':patient.hypertension,
        'heart_disease': patient.heart_disease,
        'ever_married': encoding_maps['ever_married'][patient.ever_married],
        
        'Residence_type': encoding_maps['Residence_type'][patient.residence_type],
        'avg_glucose_level': patient.avg_glucose_level,
        'bmi': patient.bmi, }
    
# For the O.HE. thingyy

    for col in feature_columns:
        if col.startswith('work_type_'):
            input_dict[col]= 1 if col == f'work_type_{patient.work_type}' else 0
        elif col.startswith('smoking_status_'):
            input_dict[col] = 1 if col == f'smoking_status_{patient.smoking_status}' else 0


    input_df = pd.DataFrame([input_dict])
    input_df = input_df.reindex(columns= feature_columns, fill_value=0)

    cols_to_scale = ['age', 'avg_glucose_level', 'bmi']
    input_df[cols_to_scale] = scaler.transform(input_df[cols_to_scale])

    selected_model = baseline_model if patient.model_choice == 'Baseline' else tuned_model
    probability = float(selected_model.predict_proba(input_df)[0][1])
    
    return probability