from views import db
from models import Task
from datetime import date

db.create_all()
temp_session=db.session
""":type: sqlalchemy.orm.Session"""
temp_session.add(Task("Finish this tutorial",date(2015,3,13),10,1))
temp_session.add(Task("Finish Real Python",date(2015,3,13),10,1))

db.session.commit()
