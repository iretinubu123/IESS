import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get script directory
dataset_path = os.path.join(BASE_DIR, "career_dataset.csv")

# Load the dataset
df = pd.read_csv(dataset_path)

# Define categorical columns
categorical_columns = ["Gender", "Favorite_Subjects", "Skills", "Extracurricular_Activities", 
                        "Personality_Traits", "Preferred_Work_Style", "Career_Outcome"]

# Encode categorical variables
encoders = {}
for col in categorical_columns:
    encoders[col] = LabelEncoder()
    df[col] = encoders[col].fit_transform(df[col])

# Ensure directory exists
encoder_path = os.path.join(BASE_DIR, "encoders.pth")
torch.save(encoders, encoder_path)
print(f"✅ Encoders saved at {encoder_path}")

# Split features and target
X = df.drop(columns=["Student_ID", "Career_Outcome"]).values  # Features
y = df["Career_Outcome"].values  # Target

# Normalize numerical data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Save scaler for future use
scaler_path = os.path.join(BASE_DIR, "scaler.pth")
torch.save(scaler, scaler_path)
print(f"✅ Scaler saved at {scaler_path}")
