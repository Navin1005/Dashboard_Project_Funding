# add_report.py

from app import app, db, Report

def add_report():
    with app.app_context():
        report = Report(user_id=1, content="This is a test report.")
        db.session.add(report)
        db.session.commit()
        print("Report added successfully")

if __name__ == '__main__':
    add_report()
