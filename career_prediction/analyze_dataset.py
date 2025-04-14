import pandas as pd
import os

# Load Dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "career_dataset.csv")
df = pd.read_csv(dataset_path)

# Check class distribution
print("Career Outcome Class Distribution:")
print(df["Career_Outcome"].value_counts())
