import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
import pickle
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "career_dataset.csv")
encoder_path = os.path.join(BASE_DIR, "encoders.pickle")  # Use .pickle
scaler_path = os.path.join(BASE_DIR, "scaler.pickle")      # Use .pickle
model_path = os.path.join(BASE_DIR, "career_model.pth")

# Load dataset
df = pd.read_csv(dataset_path)

# Define categorical columns
categorical_columns = [
    "Gender", "Favorite_Subjects", "Skills", 
    "Extracurricular_Activities", "Personality_Traits", "Preferred_Work_Style", "Career_Outcome"
]

# Encode categorical variables
encoders = {}
for col in categorical_columns:
    encoders[col] = LabelEncoder()
    df[col] = encoders[col].fit_transform(df[col])

# Save encoders using pickle
with open(encoder_path, "wb") as f:
    pickle.dump(encoders, f)

print(f"✅ Encoders saved at {encoder_path}")

# Split features & target
X = df.drop(columns=["Student_ID", "Career_Outcome"]).values
y = df["Career_Outcome"].values

# Apply SMOTE to balance class distribution
smote = SMOTE(random_state=42)
X, y = smote.fit_resample(X, y)
print("✅ Applied SMOTE to balance class distribution")

# Normalize numerical data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Save scaler using pickle
with open(scaler_path, "wb") as f:
    pickle.dump(scaler, f)

print(f"✅ Scaler saved at {scaler_path}")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)
y_test_tensor = torch.tensor(y_test, dtype=torch.long)

# Define Neural Network Model
class CareerPredictionModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(CareerPredictionModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 256)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, output_size)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.relu(self.fc3(x))
        x = self.fc4(x)  # No softmax (CrossEntropyLoss handles it)
        return x

# Model parameters
input_size = X_train.shape[1]
output_size = len(np.unique(y))

# Initialize model, loss function, and optimizer
model = CareerPredictionModel(input_size, output_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop with Early Stopping
epochs = 200
best_accuracy = 0.0
patience = 10
patience_counter = 0

for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()

    # Evaluate on the test set
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        predictions = torch.argmax(test_outputs, dim=1)
        accuracy = (predictions == y_test_tensor).float().mean().item()

    # Check for improvement
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        torch.save(model.state_dict(), model_path)  # Save best model
        patience_counter = 0
    else:
        patience_counter += 1

    # Print every 10 epochs
    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy*100:.2f}%")

    # Early stopping
    if patience_counter >= patience:
        print(f"⏳ Early stopping at epoch {epoch+1}. Best Accuracy: {best_accuracy*100:.2f}%")
        break

print(f"✅ Final Model trained and saved at {model_path}")
print(f"📊 Best Model Accuracy on Test Set: {best_accuracy*100:.2f}%")
