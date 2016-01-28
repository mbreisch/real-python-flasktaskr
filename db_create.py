from project import db
from project.models import Task,User
from datetime import date

db.create_all()
temp_session=db.session
""":type: sqlalchemy.orm.Session"""
temp_session.add(User("admin","ad@min.com","admin","admin"))
temp_session.add(Task("Finish this tutorial",date(2015,3,13),10,date(2015,2,3),1,1))
temp_session.add(Task("Finish Real Python",date(2015,3,13),10,date(2015,2,3),1,1))

db.session.commit()
