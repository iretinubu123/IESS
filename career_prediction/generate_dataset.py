import os
import pandas as pd
import random

# Define dataset path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "career_dataset.csv")

# Generate sample data
data = {
    "Student_ID": range(1, 101),  # 100 students
    "Gender": random.choices(["Male", "Female"], k=100),
    "Favorite_Subjects": random.choices(["Math", "Science", "History", "Arts", "Programming"], k=100),
    "Skills": random.choices(["Analytical", "Creative", "Logical", "Leadership", "Technical"], k=100),
    "Extracurricular_Activities": random.choices(["Sports", "Music", "Debate", "Volunteering"], k=100),
    "Personality_Traits": random.choices(["Introvert", "Extrovert", "Ambivert"], k=100),
    "Preferred_Work_Style": random.choices(["Independent", "Team-oriented", "Flexible"], k=100),
    "Career_Outcome": random.choices(["Engineer", "Doctor", "Artist", "Entrepreneur", "Scientist"], k=100)
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save dataset
df.to_csv(dataset_path, index=False)
print(f"✅ Dataset generated and saved at {dataset_path}")
