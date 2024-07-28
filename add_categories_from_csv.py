import csv
from app import db, Category, app

def load_categories_from_csv(file_path):
    categories = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            category, subcategory = row
            if category in categories:
                categories[category].append(subcategory)
            else:
                categories[category] = [subcategory]
    return categories

def add_categories_to_db(categories):
    with app.app_context():
        db.create_all()  # Create the database and the db table
        for category_name, subcategories in categories.items():
            category = Category(name=category_name, subcategories=','.join(subcategories))
            db.session.add(category)
        db.session.commit()
        print("Categories added successfully.")

if __name__ == "__main__":
    file_path = r'C:\Users\Ch Naveen\Risk_Insights_Media\Dashboard_Project_Funding\categories.csv'  # Path to your CSV file
    categories = load_categories_from_csv(file_path)
    add_categories_to_db(categories)
