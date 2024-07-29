from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import json
import os
from urllib.parse import quote as url_quote


app = Flask(__name__)
import os

app.config['SECRET_KEY'] = 'b0351af9384a13850c7c8570fa38f0cf'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:/Users/Ch Naveen/Risk_Insights_Media/Dashboard_Project_Funding/users.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False, default="Not started")
    data = db.Column(db.Text, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return "Access Denied", 403
    
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'user not found'}), 404


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
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
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
    current_user.data = json.dumps(data)
    current_user.status = "Completed"
    db.session.commit()
    return jsonify(status='success')

if __name__ == '__main__':
    app.run(debug=True)
