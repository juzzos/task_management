# Task Management System

A modern web-based task management system built with Python Flask, SQLAlchemy, and Bootstrap 5.

## Features

- User Authentication (Register, Login, Logout)
- Create, Read, Update, and Delete Tasks
- Task Priority Levels (High, Medium, Low)
- Task Status Tracking (Pending, Completed)
- Deadline Management
- Responsive Design
- Modern UI with Bootstrap 5

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd task_management
```
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Run the Flask application:
```bash
python .\app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
task_management/
├── app.py              # Main application file
├── auth.py            # Authentication routes
├── tasks.py           # Task management routes
├── requirements.txt   # Python dependencies
├── templates/         # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── edit_task.html
│   ├── login.html
│   ├── new_task.html
│   ├── register.html
│   └── task_card.html
└── README.md
```

## Usage

1. Register a new account
2. Log in with your credentials
3. Create new tasks with title, description, deadline, and priority
4. View all your tasks on the dashboard
5. Edit or delete tasks as needed
6. Mark tasks as completed
7. Filter tasks by priority and status

## Security Features

- Password hashing using Werkzeug
- User session management
- CSRF protection
- Secure user authentication
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 