import os
import unittest

from project import app, db,bcrypt
from project._config import basedir
from project.models import User

TEST_DB = 'test.db'
TEST_USER = ("Testing1", "testing@gmail.com", "python")


class UserTests(unittest.TestCase):
    # setup and teardown
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.create_user(TEST_USER[0],TEST_USER[1],TEST_USER[2])

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=bcrypt.generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post('register/', data=dict(name=name, email=email, password=password, confirm=confirm),
                             follow_redirects=True)

    def test_form_is_present_on_register_page(self):
        response = self.app.get("register/")
        self.assertIn(b"Please register to access the task list", response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register("Testing2", "test2@gmail.com", "python", "python")
        self.assertIn(b"Thanks for registering. Please login", response.data)


    def test_users_Can_login(self):
        response = self.login(TEST_USER[0],TEST_USER[2])
        self.assertIn('Welcome!', response.data)

    def test_invalid_form_data(self):
        self.register("Michael", "michael@realpython.com", "python", "python")
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password', response.data)

    def test_user_registration_error(self):
        self.app.get("/register", follow_redirects=True)
        response = self.register(TEST_USER[0], TEST_USER[1], TEST_USER[2],TEST_USER[2])
        self.assertIn(b"That username and/or email already exists", response.data)

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def test_logged_in_users_can_logout(self):
        self.login(TEST_USER[0],TEST_USER[2])
        response = self.logout()
        self.assertIn(b"Goodbye!", response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b"Goodbye!", response.data)

    def test_logged_in_user_can_access_tasks_page(self):
        self.login(TEST_USER[0],TEST_USER[2])
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add a new task", response.data)

    def test_not_logged_in_user_cannot_access_tasks_page(self):
        response = self.app.get('tasks/')
        self.assertNotEqual(response.status_code, 200)

    def test_default_user_role(self):
        self.create_user("Johnny","john@doe.com","johnny")
        users=db.session.query(User).all()
        print users
        for user in users:
            self.assertEquals(user.role,'user')

if __name__ == "__main__":
    unittest.main()