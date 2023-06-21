from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = 'recipes_user_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """

        results = connectToMySQL(cls.DB).query_db(query, data)

        return results
    
    @classmethod
    def get_user(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """

        results = connectToMySQL(cls.DB).query_db(query, data)

        return cls(results[0])
    
    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """

        results = connectToMySQL(cls.DB).query_db(query, data)

        if len(results) < 1:
            return False
        
        return cls(results[0])
    
    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters.')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters.')
            is_valid = False

        if len(user['first_name']) < 1:
            flash('First name is Required!')
            is_valid = False
        if len(user['last_name']) < 1:
            flash('Last Name is Required!')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address')
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(email)s"
            results = connectToMySQL(User.DB).query_db(query, user)
            if len(results) >= 1:
                flash('Email taken, try a different Email!')
                is_valid = False

        if len(user['password']) < 8:
            flash('Password must be at least 8 characters.')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('Password did not match!')
            is_valid = False

        return is_valid