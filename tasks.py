from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from extensions import db
from models import Task
from datetime import datetime
import os
from werkzeug.utils import secure_filename

tasks = Blueprint('tasks', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@tasks.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        priority = request.form.get('priority')
        file = request.files.get('file')

        if deadline:
            deadline = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
        
        task = Task(
            title=title,
            description=description,
            deadline=deadline,
            priority=priority,
            user_id=current_user.id
        )
        
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            task.file_path = filename
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task created successfully!')
        return redirect(url_for('dashboard'))
        
    return render_template('new_task.html')

@tasks.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('You do not have permission to edit this task.')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        deadline = request.form.get('deadline')
        if deadline:
            task.deadline = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
        task.priority = request.form.get('priority')
        task.status = request.form.get('status')
        
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            # Delete old file if it exists
            if task.file_path:
                old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], task.file_path)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            task.file_path = filename
        
        db.session.commit()
        flash('Task updated successfully!')
        return redirect(url_for('dashboard'))
        
    return render_template('edit_task.html', task=task)

@tasks.route('/task/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task.')
        return redirect(url_for('dashboard'))
    
    # Delete associated file if it exists
    if task.file_path:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], task.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('dashboard'))

@tasks.route('/task/<int:task_id>/toggle')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('You do not have permission to modify this task.')
        return redirect(url_for('dashboard'))
        
    task.status = 'completed' if task.status == 'pending' else 'pending'
    db.session.commit()
    return redirect(url_for('dashboard')) 