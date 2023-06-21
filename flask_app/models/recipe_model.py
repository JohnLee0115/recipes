from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
from flask_app.models import user_model

class Recipe:
    DB = 'recipes_user_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_cooked = data['date_cooked']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT * FROM recipes
        JOIN users
        ON users.id = recipes.user_id;
        """

        results = connectToMySQL(cls.DB).query_db(query)

        all_recipes = []

        for row in results:
            
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'password' : row['password'],
                'email' : row['email'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }

            one_recipe = cls(row)
            one_recipe.recipe_poster = user_model.User(user_data)
            all_recipes.append(one_recipe)
        
        return all_recipes
    
    @staticmethod
    def validate_recipe(new_recipe):
        is_valid = True
        if len(new_recipe['name']) < 1:
            flash('Name field is required!')
            is_valid = False
        if len(new_recipe['description']) < 1:
            flash('Description field is required!')
            is_valid = False
        if len(new_recipe['instruction']) < 1:
            flash('Instruction field is required!')
            is_valid = False
        if len(new_recipe['date_cooked']) < 1:
            flash('Date Cooked field is required!')
            is_valid = False
        if 'under_thirty' not in new_recipe:
            flash('Under 30 field is required!')
            is_valid = False
        
        return is_valid

    @classmethod
    def create_recipe(cls, data):
        query = """
        INSERT INTO recipes (name, description,
        instruction, date_cooked, under_thirty, user_id)
        VALUES (%(name)s, %(description)s, %(instruction)s,
        %(date_cooked)s, %(under_thirty)s, %(user_id)s);
        """

        results = connectToMySQL(cls.DB).query_db(query, data)

        return results
    
    @classmethod
    def get_one_recipe(cls, data):
        query = """
        SELECT * FROM recipes
        JOIN users ON users.id = recipes.user_id
        WHERE recipes.id = %(recipe_id)s;
        """

        results = connectToMySQL(cls.DB).query_db(query, data)

        one_recipe = cls(results[0])

        user_data = {
                'id' : results[0]['users.id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'password' : results[0]['password'],
                'email' : results[0]['email'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            }

        one_recipe.recipe_poster = user_model.User(user_data)

        return one_recipe
    
    @classmethod
    def update_recipe(cls, data):
        query = """
        UPDATE recipes
        SET name = %(name)s,
        description = %(description)s,
        instruction = %(instruction)s,
        date_cooked = %(date_cooked)s,
        under_thirty = %(under_thirty)s
        WHERE id = %(recipe_id)s;
        """

        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def recipe_delete(cls, data):
        query = """
        DELETE FROM recipes
        WHERE id = %(recipe_id)s;
        """

        return connectToMySQL(cls.DB).query_db(query, data)