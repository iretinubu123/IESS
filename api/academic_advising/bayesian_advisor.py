import os
import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

# Set Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "academic_data.csv")

# Load Dataset
df = pd.read_csv(dataset_path)

# Define Bayesian Network structure
model = BayesianNetwork([
    ("GPA", "Recommended_Course"),
    ("Study_Habits", "GPA"),
    ("Interest_in_Subjects", "Recommended_Course"),
])

# Train Model using Maximum Likelihood Estimation
model.fit(df, estimator=MaximumLikelihoodEstimator)

# Inference Engine
inference = VariableElimination(model)

# Function to predict recommended courses
def recommend_course(gpa, study_habits, interest):
    query_result = inference.map_query(
        variables=["Recommended_Course"],
        evidence={"GPA": gpa, "Study_Habits": study_habits, "Interest_in_Subjects": interest}
    )
    return query_result["Recommended_Course"]

# Example Usage
if __name__ == "__main__":
    recommended = recommend_course(gpa="High", study_habits="Visual", interest="Mathematics")
    print(f"📚 Recommended Course: {recommended}")
