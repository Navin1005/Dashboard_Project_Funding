import sqlite3

# Path to your SQLite database file
db_path = 'C:\\Users\\Ch Naveen\\Risk_Insights_Media\\Dashboard_Project_Funding\\instance\\users.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch all users
cursor.execute('SELECT id, user_id, username, is_admin, status FROM user')
users = cursor.fetchall()

# Print user details
for user in users:
    print(f"ID: {user[0]}, User ID: {user[1]}, Username: {user[2]}, Is Admin: {user[3]}, Status: {user[4]}")

# Close the connection
conn.close()
