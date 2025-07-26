from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
db = client.event_management
users_collection = db.users
events_collection = db.events
attendees_collection = db.attendees
tasks_collection = db.tasks

# User Class
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(user_id=str(user['_id']), username=user['username'])
    return None

# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users_collection.find_one({"username": username}):
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_collection.insert_one({"username": username, "password_hash": hashed_password})
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))  # Redirect clears form data
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({"username": username})

        if user and bcrypt.check_password_hash(user['password_hash'], password):
            login_user(User(user_id=str(user['_id']), username=user['username']))
            flash("Login successful!", "success")
            return redirect(url_for('event_management'))  # Redirect clears form data
        else:
            flash("Invalid credentials, please try again.", "danger")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

# Dashboard and Protected Routes
@app.route('/')
@login_required
def home():
    return render_template('base.html')

# Event Management
@app.route('/event_management')
@login_required
def event_management():
    events = list(events_collection.find())
    return render_template('event_management.html', events=events)

@app.route('/create_event', methods=['POST'])
@login_required
def create_event():
    data = request.form
    new_event = {
        "name": data['name'],
        "date": data['date'],
        "description": data['description'],
        "location": data['location']
    }
    events_collection.insert_one(new_event)
    return redirect(url_for('event_management'))

@app.route('/delete_event/<event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    events_collection.delete_one({"_id": ObjectId(event_id)})
    return redirect(url_for('event_management'))

# Attendee Management
@app.route('/attendee_management')
@login_required
def attendee_management():
    attendees = list(attendees_collection.find())
    events = list(events_collection.find())
    return render_template('attendee_management.html', attendees=attendees, events=events)

@app.route('/add_attendee', methods=['POST'])
@login_required
def add_attendee():
    data = request.form
    new_attendee = {
        "name": data['name'],
        "event_id": ObjectId(data['event_id']) if data.get('event_id') else None
    }
    attendees_collection.insert_one(new_attendee)
    return redirect(url_for('attendee_management'))

@app.route('/remove_attendee/<attendee_id>', methods=['POST'])
@login_required
def remove_attendee(attendee_id):
    attendees_collection.delete_one({"_id": ObjectId(attendee_id)})
    return redirect(url_for('attendee_management'))

# Task Tracker
@app.route('/task_tracker')
@login_required
def task_tracker():
    tasks = list(tasks_collection.find())
    events = list(events_collection.find())
    return render_template('task_tracker.html', tasks=tasks, events=events)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    data = request.form
    new_task = {
        "title": data['title'],
        "description": data['description'],
        "event_id": ObjectId(data['event_id']) if data.get('event_id') else None
    }
    tasks_collection.insert_one(new_task)
    return redirect(url_for('task_tracker'))

@app.route('/delete_task/<task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect(url_for('task_tracker'))

if __name__ == '__main__':
    app.run(debug=True)
