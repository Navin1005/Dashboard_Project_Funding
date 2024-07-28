import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/Ch Naveen/Risk_Insights_Media/Dashboard_Project_Funding/users.db')
cursor = conn.cursor()

# Update the is_admin field for the admin user
cursor.execute("UPDATE user SET is_admin = 1 WHERE username = 'admin'")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Admin user updated successfully.")
