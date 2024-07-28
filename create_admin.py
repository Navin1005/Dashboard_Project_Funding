
from app import app  # Ensure the Flask app context is available
from app import db, User

with app.app_context():
    # Create an admin user
    admin_user = User(username='admin', password='admin', status='Not started', is_admin=True)

    # Add the admin user to the session and commit
    db.session.add(admin_user)
    db.session.commit()

    print("Admin user created successfully.")
