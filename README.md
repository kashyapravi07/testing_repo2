# Event Management Dashboard

A full-featured Event Management Dashboard built using Flask and MongoDB. This application allows users to manage events, attendees, and tasks, with user-specific data visibility and secure login and registration features.


<a href ="https://www.youtube.com/watch?v=WZ4qFp_NRbg">Complete Demonstration video of the project</a>
## Features

- **User Authentication**: Secure login and registration using Flask-Login and Flask-Bcrypt.
- **Event Management**: Create, view, and delete events.
- **Attendee Management**: Add and remove attendees linked to specific events.
- **Task Tracker**: Assign tasks to events and manage them effectively.
- **Data Security**: Users can only view and manage data they create.

## Installation and Setup

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/kashyapravi07/WebKnot-Assignment.git
cd WebKnot-Assignment
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB
- Install and start MongoDB on your system (installation guide)
- Create a database named `event_management`
- The following collections will be used:
  - `users`
  - `events`
  - `attendees`
  - `tasks`

Note: No manual setup for collections is needed as the application will create them automatically during usage.

### 5. Run the Application
Start the Flask development server:
```bash
python app.py
```

### 6. Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

## Folder Structure
```
event-management-dashboard/
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── scripts.js
├── templates/
│   ├── base.html
│   ├── register.html
│   ├── login.html
│   ├── event_management.html
│   ├── attendee_management.html
│   └── task_tracker.html
├── app.py
├── requirements.txt
└── README.md
```

## Usage

### Registration
1. Navigate to the registration page
2. Enter your desired username and password
3. After successful registration, log in with your credentials

### Event Management
1. Go to the **Event Management** section
2. Create new events by filling out the form
3. View and delete events you have created

### Attendee Management
1. Navigate to the **Attendee Management** section
2. Add attendees by linking them to specific events
3. Remove attendees as needed

### Task Tracker
1. Access the **Task Tracker** section
2. Assign tasks to events and manage them effectively

## Tech Stack
- **Backend**: Flask
- **Database**: MongoDB
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Flask-Login, Flask-Bcrypt
