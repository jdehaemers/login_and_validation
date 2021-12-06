from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id == data['id']
        self.first_name == data['first_name']
        self.last_name == data['last_name']
        self.email == data['email']
        self.password == data['password']
        self.created_at == data['created_at']
        self.updated_at == data['updated_at']
    
    @classmethod
    def create(self, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );'
        return connectToMySQL('login_and_validation_schema').query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL('login_and_validation_schema').query_db(query)
        return results
    
    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('login_and_validation_schema').query_db(query, data)
        print('---------')
        print(results)
        if len(results) == 0:
            return False
        else:
            return results[0]
    
    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address")
            is_valid = False
        users = User.get_all()
        for u in users:
            if user['email'] == u['email']:
                flash("Non-unique email address")
                is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords must match')
            is_valid = False
        if len(user['password']) < 5:
            flash('Password must be at least 2 characters')
            is_valid = False
        return is_valid