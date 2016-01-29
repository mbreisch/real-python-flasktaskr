# project/users/views.py

# imports

from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm, LoginForm
from project import db
from project.models import User

# config
users_blueprint = Blueprint('users', __name__)


# helper functions

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for('users.login'))

    return wrap


@users_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('name',None)
    flash("Goodbye!")
    return redirect(url_for('users.login'))


@users_blueprint.route('/', methods=['POST', 'GET'])
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
                session['name']=user.name
                flash("Welcome!")
                return redirect(url_for('tasks.tasks'))
            else:
                error = 'Invalid username or password'
    return render_template("login.html", form=form, error=error)


@users_blueprint.route('/register/', methods=['GET', 'POST'])
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
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = 'That username and/or email already exists'
                return render_template('register.html', form=form, error=error)

    return render_template('register.html', form=form, error=error)
