import pandas as pd
import json

# Load the CSV file
file_path = 'C:/Users/Ch Naveen/Risk_Insights_Media/Dashboard_Project_Funding/categories.csv'  # Update with the correct path to your CSV file
df = pd.read_csv(file_path)

# Convert CSV data to dictionary
categories = {}
for _, row in df.iterrows():
    category = row['Category-Group']
    subcategory = row['SUBCATEGORIES']
    if category not in categories:
        categories[category] = []
    categories[category].append(subcategory)

# Save the data to a JSON file
with open('static/categories.json', 'w') as json_file:
    json.dump(categories, json_file)

print("JSON file created successfully.")
