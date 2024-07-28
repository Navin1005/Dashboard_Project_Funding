from app import db, User, app

with app.app_context():
    db.create_all()  # Create the database and the db table

    # Insert user data
    admin = User(username='admin', password='adminpass', is_admin=True)
    expert = User(username='expert', password='expertpass', is_admin=False)

    # Add user data to the session
    db.session.add(admin)
    db.session.add(expert)

    # Commit the changes to the database
    db.session.commit()

    print("Users added successfully.")
