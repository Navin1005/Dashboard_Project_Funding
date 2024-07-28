import sqlite3
import uuid

# Path to your SQLite database file
db_path = 'C:\\Users\\Ch Naveen\\Risk_Insights_Media\\Dashboard_Project_Funding\\instance\\users.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add the user_id column to the user table
try:
    cursor.execute('ALTER TABLE user ADD COLUMN user_id TEXT UNIQUE')
except sqlite3.OperationalError as e:
    print("Error adding user_id column:", e)

# Generate and populate the user_id for existing users
cursor.execute('SELECT id FROM user')
users = cursor.fetchall()

for user in users:
    user_id = str(uuid.uuid4())
    cursor.execute('UPDATE user SET user_id = ? WHERE id = ?', (user_id, user[0]))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("user_id column added and populated successfully.")
