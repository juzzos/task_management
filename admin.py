from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import User, Task
import os

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_administrator():
            flash('You need to be an administrator to access this page.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    users = User.query.all()
    tasks = Task.query.all()
    return render_template('admin/dashboard.html', users=users, tasks=tasks)

@admin.route('/admin/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/admin/user/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot modify your own admin status.')
        return redirect(url_for('admin.manage_users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'Admin status for {user.username} has been {"granted" if user.is_admin else "revoked"}.')
    return redirect(url_for('admin.manage_users'))

@admin.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot delete your own account.')
        return redirect(url_for('admin.manage_users'))
    
    # Delete user's tasks and associated files
    for task in user.tasks:
        if task.file_path:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], task.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
    
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} has been deleted.')
    return redirect(url_for('admin.manage_users'))

@admin.route('/admin/tasks')
@login_required
@admin_required
def manage_tasks():
    tasks = Task.query.all()
    return render_template('admin/tasks.html', tasks=tasks) 