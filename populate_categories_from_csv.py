import sqlite3
import csv

# Path to your SQLite database file
db_path = 'C:\\Users\\Ch Naveen\\Risk_Insights_Media\\Dashboard_Project_Funding\\users.db'

# Path to your CSV file
csv_path = 'C:\\Users\\Ch Naveen\\Risk_Insights_Media\\Dashboard_Project_Funding\\categories.csv'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the category table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subcategories TEXT NOT NULL
)
''')

# Read data from CSV and insert into the category table
with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
    csvreader = csv.DictReader(csvfile)
    print(f"CSV Headers: {csvreader.fieldnames}")  # Debugging line
    for row in csvreader:
        print(f"Row Data: {row}")  # Debugging line
        cursor.execute('INSERT INTO category (name, subcategories) VALUES (?, ?)', (row['name'], row['subcategories']))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Categories populated from CSV successfully.")
