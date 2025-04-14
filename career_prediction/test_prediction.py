from api.career_prediction.model_utils import predict_career

# Example student data (ensure these match the dataset columns)
student_data = {
    "Gender": "Male",
    "Favorite_Subjects": "Math",
    "Skills": "Problem-Solving",
    "Extracurricular_Activities": "Robotics",
    "Personality_Traits": "Analytical",
    "Preferred_Work_Style": "Independent"
}

student_data = {
    "Gender": "Female",
    "Favorite_Subjects": "Science",
    "Skills": "Writing",
    "Extracurricular_Activities": "Music",
    "Personality_Traits": "Extrovert",
    "Preferred_Work_Style": "Hybrid",
}
predicted_career = predict_career(student_data)
print(f"Predicted Career ID: {predicted_career}")

# Predict career
predicted_career = predict_career(student_data)

print(f"Predicted Career ID: {predicted_career}")
