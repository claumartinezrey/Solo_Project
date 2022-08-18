from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re

class Movement:
    db = "workout_routines"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.user_id = data['user_id']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # VALIDATIONS TO BE ENTERED HERE
    @staticmethod
    def validate_movement(movement):
        is_valid = True
        # checking name length
        if len(movement['name']) < 2:
            flash("Name must contain at least 2 characters", "new_movement_error")
            is_valid = False
        
        query = "SELECT * FROM movements WHERE name = %(name)s"
        results = connectToMySQL(Movement.db).query_db(query, movement)
        if len(results) >= 1:
            flash("Name is already in use", "new_movement_error")
            is_valid = False
        return is_valid



    @staticmethod
    def validate_updated_movement(movement):
        is_valid = True
        # checking name length
        if len(movement['name']) < 2:
            flash("Name must contain at least 2 characters", "update_movement_error")
            is_valid = False
        
        query = "SELECT * FROM movements WHERE name = %(name)s"
        results = connectToMySQL(Movement.db).query_db(query, movement)
        data = {
            "id": movement['id']
        }
        my_movements = Movement.get_by_id(data)
        if my_movements.name == movement['name']:
            pass
        elif len(results) >= 1:
            flash("Name is already in use", "update_movement_error")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO movements (name, description, user_id, created_at, updated_at) VALUES ( %(name)s, %(description)s, %(user_id)s, NOW(), NOW() );"
        return connectToMySQL(Movement.db).query_db(query, data)

    @classmethod
    def delete_by_id(cls,data):
        query = "DELETE FROM movements WHERE id = %(id)s"
        return connectToMySQL(Movement.db).query_db(query, data)

    @classmethod
    def update(cls,data):
        query = "UPDATE movements SET name=%(name)s, description=%(description)s, user_id=%(user_id)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(Movement.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM movements;"
        results = connectToMySQL(Movement.db).query_db(query)
        movements = []
        for movement in results:
            movements.append( cls(movement))
        return movements

    @classmethod
    def get_all_movements_by_user_id(cls, data):
        query = "SELECT * FROM movements WHERE user_id = %(id)s;"
        results = connectToMySQL(Movement.db).query_db(query, data)
        movements = []
        for movement in results:
            movements.append( cls(movement))
        return movements
    
    @classmethod
    def get_name_by_id(cls, data):
        query = "SELECT name FROM movements WHERE id = %(id)s;"
        results = connectToMySQL(Movement.db).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_id_by_name(cls, data):
        query = "SELECT id FROM movements WHERE name = %(name)s;"
        results = connectToMySQL(Movement.db).query_db(query, data)
        return results
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM movements WHERE id = %(id)s;"
        results = connectToMySQL(Movement.db).query_db(query, data)
        return cls(results[0])