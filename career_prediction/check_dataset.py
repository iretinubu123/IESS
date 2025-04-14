import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "career_dataset.csv")

# Load dataset
df = pd.read_csv(dataset_path)

#  Check if dataset is balanced
plt.figure(figsize=(10, 6))
sns.countplot(x="Career_Outcome", data=df)
plt.title("Career Outcome Distribution")
plt.xticks(rotation=45)
plt.show()

#  Print dataset stats
print("\n🔍 Dataset Summary:")
print(df.describe())

#  Check for duplicate rows
print(f"\n🔍 Checking for duplicate rows: {df.duplicated().sum()} found")

# Check for missing values
print("\n🔍 Checking for missing values:")
print(df.isnull().sum())

print("\n Data check completed.")
