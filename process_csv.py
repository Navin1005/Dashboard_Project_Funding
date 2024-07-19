import pandas as pd
import json

# Load the CSV file
file_path = 'categories.csv'  # Update with the correct path to your CSV file
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
with open('categories.json', 'w') as json_file:
    json.dump(categories, json_file)

print("JSON file created successfully.")
