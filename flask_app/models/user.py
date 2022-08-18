from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
#from flask_app.models import sighting
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')

class User:
    db = "workout_routines"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.movements = []
        self.workouts = []
        self.workouts_completed = []

    @staticmethod
    def validate_user(user):
        is_valid = True
        # checking first name lenght
        if len(user['first_name']) < 2:
            flash("First Name must contain at least 2 characters", "register_error")
            is_valid = False
        
        # checking last name lenght
        if len(user['last_name']) < 2:
            flash("Last Name must contain at least 2 characters", "register_error")
            is_valid = False
        
        # checkin email is not already in the database
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is not valid!", "register_error")
            is_valid = False
        if len(results) >= 1:
            flash("Email is already in use", "register_error")
            is_valid = False
        
        #checking password
        if len(user['password']) < 8:
            flash("Password must contain at least 8 characters", "register_error")
            is_valid = False
        if (user['password'] != user['confirm_password']):
            flash("Passwords must match!", "register_error")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user_edited(user):
        is_valid = True
        # checking first name lenght
        if len(user['first_name']) < 2:
            flash("First Name must contain at least 2 characters", "register_error")
            is_valid = False
        
        # checking last name lenght
        if len(user['last_name']) < 2:
            flash("Last Name must contain at least 2 characters", "register_error")
            is_valid = False
        
        # CHECK IF EMAIL ENTERED MATCHES EMAIL OF USER LOGGED IN
        # if the email matches with user logged in then no error will be shown
        # if the email doesn't match, then we will check that the new email
        # is not already in use by another user
        query2 = "SELECT * FROM users WHERE email = %(email)s;"
        results2 = connectToMySQL(User.db).query_db(query2, user)
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is not valid!", "register_error")
            is_valid = False
        data = {
            "id": user['id']
        }
        my_users = User.get_by_id(data)
        if my_users.email == user['email']:
            pass
        elif len(results2) >= 1:
            flash("Email is already in use", "register_error")
            is_valid = False
        
        #checking password
        if len(user['password']) < 8:
            flash("Password must contain at least 8 characters", "register_error")
            is_valid = False
        if (user['password'] != user['confirm_password']):
            flash("Passwords must match!", "register_error")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        return connectToMySQL(User.db).query_db(query, data)

    @classmethod
    def delete(cls,data):
        pass

    @classmethod
    def update_user_by_id(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(User.db).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(User.db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s ;"
        results = connectToMySQL(User.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(User.db).query_db(query, data)
        return cls(results[0])
    
    