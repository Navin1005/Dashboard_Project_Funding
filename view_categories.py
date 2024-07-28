from app import db, Category, app

with app.app_context():
    categories = Category.query.all()
    for category in categories:
        print(f"Category: {category.name}, Subcategories: {category.subcategories}")
