import os
import torch
import torch.nn as nn
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

#  Define Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "career_model.pth")
ENCODER_PATH = os.path.join(BASE_DIR, "encoders.pth")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pth")

# Define the same model architecture
class CareerPredictionModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(CareerPredictionModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)
        x = self.relu(self.fc3(x))
        x = self.fc4(x)
        return x

#  Load Model & Data Transformers
def load_model():
    encoders = torch.load(ENCODER_PATH)
    scaler = torch.load(SCALER_PATH)

    input_size = len(scaler.mean_)
    output_size = len(encoders["Career_Outcome"].classes_)

    model = CareerPredictionModel(input_size, output_size)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
    model.eval()
    return model, encoders, scaler

#  Predict Career
def predict_career(student_data):
    model, encoders, scaler = load_model()

    student_df = pd.DataFrame([student_data])
    for col in encoders.keys():
        student_df[col] = encoders[col].transform(student_df[col])

    student_features = scaler.transform(student_df.values)
    student_tensor = torch.tensor(student_features, dtype=torch.float32)

    with torch.no_grad():
        output = model(student_tensor)
        predicted_class = torch.argmax(output, dim=1).item()

    return encoders["Career_Outcome"].inverse_transform([predicted_class])[0]
