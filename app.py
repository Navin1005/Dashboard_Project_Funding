from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from datetime import datetime
import pandas as pd
import json
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b0351af9384a13850c7c8570fa38f0cf'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:/Users/Ch Naveen/Risk_Insights_Media/Dashboard_Project_Funding/users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False, default='Not started')  # Ensure default is a string constant
    data = db.Column(db.Text, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref=db.backref('reports', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        # Delete all reports associated with the user
        reports = Report.query.filter_by(user_id=user_id).all()
        for report in reports:
            db.session.delete(report)
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin'))


@app.route('/update_status', methods=['POST'])
@login_required
def update_status():
    current_user.status = request.json['status']
    db.session.commit()
    return jsonify(status='success')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('dashboard'))
        return 'Invalid username or password!'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return 'User already exists!'
        new_user = User(username=username, password=password, is_admin=False)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Load the CSV file
    df = pd.read_csv('static/categories.csv')

    # Convert CSV data to dictionary
    categories = {}
    for _, row in df.iterrows():
        category = row['Category-Group']
        subcategory = row['SUBCATEGORIES']
        if category not in categories:
            categories[category] = []
        categories[category].append(subcategory)

    return render_template('dashboard.html', username=current_user.username, categories=json.dumps(categories))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return "Access Denied", 403
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/admin/reports')
@login_required
def admin_reports():
    if not current_user.is_admin:
        return "Access Denied", 403
    reports = Report.query.all()
    return render_template('admin_reports.html', reports=reports)

@app.route('/submit_report', methods=['GET', 'POST'])
@login_required
def submit_report():
    if request.method == 'POST':
        content = request.form['content']
        report = Report(content=content, user_id=current_user.id)
        db.session.add(report)
        current_user.status = 'Completed'  # Update status to Completed
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('submit_report.html')

@app.route('/data')
@login_required
def data():
    df = pd.read_csv('static/categories.csv')
    categories = {}
    for _, row in df.iterrows():
        category = row['Category-Group']
        subcategory = row['SUBCATEGORIES']
        if category not in categories:
            categories[category] = []
        categories[category].append(subcategory)
    
    user_data = {}
    if current_user.data:
        user_data = json.loads(current_user.data)
    
    return jsonify(categories=categories, user_data=user_data)

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    data = request.json
    # Convert the categorization data to a string or JSON format
    report_content = json.dumps(data)
    # Create a new report entry
    new_report = Report(user_id=current_user.id, content=report_content)
    db.session.add(new_report)
    db.session.commit()
    current_user.status = "Completed"
    db.session.commit()
    return jsonify(status='success')

if __name__ == '__main__':
    app.run(debug=True)
