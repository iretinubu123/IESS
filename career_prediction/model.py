import torch
import os

# Define the career prediction model architecture (same as training)
class CareerPredictionModel(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(CareerPredictionModel, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, 128)
        self.fc2 = torch.nn.Linear(128, 64)
        self.fc3 = torch.nn.Linear(64, output_size)
        self.relu = torch.nn.ReLU()
        self.softmax = torch.nn.Softmax(dim=1)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.softmax(self.fc3(x))
        return x

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), "trained_model.pth")
model = CareerPredictionModel(input_size=10, output_size=5)  # Adjust based on training
model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
model.eval()

# Define career labels (should match training labels)
career_labels = ["AI Engineer", "Data Scientist", "Cybersecurity Analyst", "Web Developer", "Financial Analyst"]
