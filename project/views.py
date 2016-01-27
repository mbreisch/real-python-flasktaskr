from functools import wraps

import datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for
from forms import AddTaskForm, RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# config
app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)
from models import Task, User


# helper functions

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for('login'))

    return wrap


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


def open_tasks():
    return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())


# route handlers

@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    flash("Goodbye!")
    return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            query = User.query
            """:type: sqlalchemy.orm.Query"""
            user = query.filter_by(name=request.form['name']).first()
            if user is not None and user.password == request.form['password']:
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = user.role
                flash("Welcome!")
                return redirect(url_for('tasks'))
            else:
                error = 'Invalid username or password'
    return render_template("login.html", form=form, error=error)


@app.route('/tasks/')
@login_required
def tasks():
    return render_template('tasks.html', form=AddTaskForm(request.form), open_tasks=open_tasks(),
                           closed_tasks=closed_tasks())


@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    error = None
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(
                    form.name.data,
                    form.due_date.data,
                    form.priority.data,
                    datetime.datetime.utcnow(),
                    '1',
                    session['user_id']
            )
            temp_session = db.session
            """:type: sqlalchemy.orm.Session"""
            temp_session.add(new_task)
            temp_session.commit()
            flash('New entry was successfully posted. Thanks.')
            return redirect(url_for('tasks'))

    return render_template('tasks.html', form=form, error=error, open_tasks=open_tasks(), closed_tasks=closed_tasks())


@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        task.update({"status": 0})
        db.session.commit()
        flash('The task was marked as complete. Nice')
        return redirect(url_for('tasks'))
    else:
        flash("You can only update tasks that belong to you.")
        return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        task.update({"status": 0})
        db.session.commit()
        flash('The task was deleted. Why not add a new one?')
        return redirect(url_for('tasks'))
    else:
        flash("You can only delete tasks that belong to you.")
        return redirect(url_for('tasks'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(form.name.data, form.email.data, form.password.data)
            temp_session = db.session
            """:type: sqlalchemy.orm.Session"""
            try:
                temp_session.add(new_user)
                temp_session.commit()
                flash("Thanks for registering. Please login.")
                return redirect(url_for('login'))
            except IntegrityError:
                error = 'That username and/or email already exists'
                return render_template('register.html', form=form, error=error)

    return render_template('register.html', form=form, error=error)
