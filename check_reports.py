# check_reports.py

from app import app, db, Report

def check_reports():
    with app.app_context():
        reports = Report.query.all()
        for report in reports:
            print(f"User ID: {report.user_id}, Content: {report.content}, Timestamp: {report.timestamp}")

if __name__ == '__main__':
    check_reports()
