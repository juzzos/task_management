import os
from app import create_app, db
from models import User

def reset_database():
    # Get the app context
    app = create_app()
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        
        # Add admin to database
        db.session.add(admin)
        db.session.commit()
        
        print('Database has been reset!')
        print('Created default admin user:')
        print('Username: admin')
        print('Password: admin123')

if __name__ == '__main__':
    reset_database() 