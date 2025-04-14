import os
import torch
import pandas as pd
import numpy as np
import pickle
from .train_model import CareerPredictionModel

# Load paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "career_model.pth")
ENCODER_PATH = os.path.join(BASE_DIR, "encoders.pickle")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pickle")
DATASET_PATH = os.path.join(BASE_DIR, "career_dataset.csv")  # Load dataset

# Load dataset to determine input size dynamically
df = pd.read_csv(DATASET_PATH)
feature_columns = df.drop(columns=["Student_ID", "Career_Outcome"]).columns
input_size = len(feature_columns)

# Load encoders & scaler using pickle
with open(ENCODER_PATH, "rb") as f:
    encoders = pickle.load(f)

with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

# Load model with correct input size
output_size = len(encoders["Career_Outcome"].classes_)  # Get number of classes
model = CareerPredictionModel(input_size, output_size)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
model.eval()

# Define categorical columns
categorical_columns = [
    "Gender", "Favorite_Subjects", "Skills", 
    "Extracurricular_Activities", "Personality_Traits", "Preferred_Work_Style"
]

def predict_career(student_data):
    student_df = pd.DataFrame([student_data])

    # Handle unseen labels
    for col in categorical_columns:
        if col in student_df.columns and col in encoders:
            student_df[col] = student_df[col].apply(
                lambda x: encoders[col].transform([x])[0] if x in encoders[col].classes_ else -1
            )
        else:
            student_df[col] = -1  # Assign default if encoder is missing

    # Convert to numpy and scale numerical features
    student_features = scaler.transform(student_df.values)

    # Convert to tensor for prediction
    student_tensor = torch.tensor(student_features, dtype=torch.float32)

    # Make prediction
    with torch.no_grad():
        output = model(student_tensor)
        predicted_index = torch.argmax(output, dim=1).item()

    # Get career labels
    career_labels = encoders["Career_Outcome"].classes_
    predicted_career = career_labels[predicted_index]

    return predicted_career
