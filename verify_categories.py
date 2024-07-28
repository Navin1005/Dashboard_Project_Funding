import sqlite3

# Path to your SQLite database file
db_path = 'C:\\Users\\Ch Naveen\\Risk_Insights_Media\\Dashboard_Project_Funding\\users.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch all categories
cursor.execute('SELECT id, name, subcategories FROM category')
categories = cursor.fetchall()

# Print category details
for category in categories:
    print(f"ID: {category[0]}, Name: {category[1]}, Subcategories: {category[2]}")

# Close the connection
conn.close()
