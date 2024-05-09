from flask import render_template, flash, redirect, url_for, request, abort
from task_manager.webform import UserForm, TaskForm, LoginForm, DeleteForm
from task_manager.model import User, Task
from task_manager import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

db.create_all()

# user_task = [{'id':1, 'task_name':'cook', 'task_description':'cook yam and egg', 'due_date':'idk'}, 
#             {'id':2,'task_name':'cook', 'task_description':'cook yam and egg', 'due_date':'idk'}]

@app.route('/', methods=['POST', 'GET'])
def task_list():
    if current_user.is_authenticated:
        task = Task
        user_task = current_user.task
        return render_template('task_list.html', tasks=user_task, title='Task Manager')
    else:
        # flash('Please Login or Create and account to Create Tasks')
        return render_template('task_list.html')

    
    
    
@app.route('/tasks/<int:task_id>')
def actual_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('actual_task.html', task=task, title='Task Manager')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('task_list'))
    register = UserForm()
    if register.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(register.password.data).decode('utf-8')
        user = User(name=register.name.data, email=register.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has ben created, you can login now!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=register, title='Register')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('task_list'))
    login = LoginForm()
    if login.validate_on_submit():
        user = User.query.filter_by(email=login.email.data).first()
        if user and bcrypt.check_password_hash( user.password, login.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('task_list'))
        else:
            flash('Login unsuccesful, email or password is incorrect')
    return render_template('login.html', form=login, title='Login')

@app.route('/logout') 
def logout():
    logout_user()
    return redirect(url_for('task_list'))



@app.route('/create_task', methods=['POST', 'GET'])
@login_required
def create_task():
    task = TaskForm()
    if task.validate_on_submit():
        if current_user.is_authenticated:
            task_db = Task(task_name=task.task_name.data, task_description=task.task_description.data, user=current_user)
            db.session.add(task_db)
            db.session.commit()
            flash('Task has been created!')
            return redirect(url_for('task_list'))
        else:
            flash('Please Login or Create and account to Create Tasks')
            return redirect(url_for('task_list'))
    return render_template('create_task.html', form=task, legend='NEW TASK', title='Create Task')

@app.route('/tasks/<int:task_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)
    task_form = TaskForm()
    if task_form.validate_on_submit():
        task.task_name = task_form.task_name.data
        task.task_description = task_form.task_description.data
        db.session.commit()
        flash('Task has been updated')
        return redirect(url_for('actual_task', task_id=task.id))
    elif request.method == 'GET':
        task_form.task_description.data = task.task_description
        task_form.task_name.data = task.task_name
    return render_template('create_task.html', form=task_form, legend='EDIT TASK', title='Edit Task')

@app.route('/tasks/<int:task_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    delete_task = DeleteForm()
    task_by_id = task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)
    if delete_task.validate_on_submit():
        db.session.delete(task_by_id)
        db.session.commit()
        flash('Task has been deleted')
        return redirect('/')
    return render_template('delete.html',task=task_by_id,  form=delete_task, title='Delete Task')

@app.route('/profile')
@login_required
def profile():
    if current_user in User.query.all():
        return render_template('profile.html')
    else:
        flash('Please create an account')
        return redirect('/')
    