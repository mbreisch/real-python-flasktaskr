import os

# Grab directory where thi script lives
basedir=os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY='\x07\xdd\xb7\x1e\xe8\x1d*\xe3`3\xa2\x9e\xf6\x94\xd4i\x14(\xa7\x93\xe5s\n\x8e'

# Define full path for the database
DATABASE_PATH=os.path.join(basedir,DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH

