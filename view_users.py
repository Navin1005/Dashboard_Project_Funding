from app import db, User, app

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"Username: {user.username}, Password: {user.password}, Is Admin: {user.is_admin}")
