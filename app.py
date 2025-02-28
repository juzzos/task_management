from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_login import current_user, login_required
import os
from extensions import db, login_manager, mail
from models import User, Task

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.titan.email'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'no-reply@rubricsystem.com'
    app.config['MAIL_PASSWORD'] = 'o6VSK0cjvDa~'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@rubricsystem.com'

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)

    # Create uploads directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from auth import auth as auth_blueprint
    from tasks import tasks as tasks_blueprint
    from admin import admin as admin_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(tasks_blueprint)
    app.register_blueprint(admin_blueprint)

    # Routes
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('index.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
        return render_template('dashboard.html', tasks=tasks)

    @app.route('/uploads/<filename>')
    @login_required
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create the first admin user if no users exist
        if not User.query.first():
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Created default admin user:')
            print('Username: admin')
            print('Password: admin123')
    app.run(debug=True) 