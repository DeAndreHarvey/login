""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

class WelcomeModel(Model):
    def __init__(self):
        super(WelcomeModel, self).__init__()
        
        
    def create_user(self, info):
        
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        
        if len(info['fname']) < 2:
            errors.append('First name must be at least 2 characters long')
        elif len(info['lname']) < 2:
            errors.append(' Last name must be at least 2 characters long')    
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pw_confirmation']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = info['password']
            pw_hash = self.bcrypt.generate_password_hash(password)
            create_query = "INSERT INTO users (email, first_name,last_name, pw_hash, created_at) VALUES (:email, :fname, :lname, :pw_hash, NOW())"
            create_data = { 'email': info['email'], 'fname': info['fname'], 'lname':info['lname'], 'pw_hash': pw_hash }
            self.db.query_db(create_query, create_data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return { "status": True, "user": users[0] }
    def login_user(self, info):
        password = info['password']
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        user = self.db.query_db(user_query, user_data)
        print user
        if user:
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):
                return { "status": True, "user": user[0] }
        return {"status": False}
        