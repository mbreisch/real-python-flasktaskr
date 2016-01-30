# project/__init__.py

from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

app = Flask(__name__)
app.config.from_pyfile('_config.py')
bcrypt=Bcrypt(app)
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint

# register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)

@app.errorhandler(404)
def page_not_found(error):
    if not app.debug:
        now= datetime.datetime.now()
        r=request.url
        with open('error.log','a') as f:
            current_timestamp=now.strftime("%d-%m-%Y %H:%M:%S")
            f.write("\n404  error at {}: {}".format(current_timestamp,r))
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
    if not app.debug:
        now= datetime.datetime.now()
        r=request.url
        with open('error.log','a') as f:
            current_timestamp=now.strftime("%d-%m-%Y %H:%M:%S")
            f.write("\n500  error at {}: {}".format(current_timestamp,r))
    return render_template('500.html'),500
