from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re

class Workout:
    db = "workout_routines"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.user_id = data['user_id']
        
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.movements_completed = []
    
    # VALIDATIONS
    @staticmethod
    def validate_workout(workout):
        is_valid = True
        # checking name length
        if len(workout['name']) < 2:
            flash("Name must contain at least 2 characters", "new_workout_error")
            is_valid = False
        
        query = "SELECT * FROM workouts WHERE name = %(name)s"
        results = connectToMySQL(Workout.db).query_db(query, workout)
        if len(results) >= 1:
            flash("Name is already in use", "new_workout_error")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_updated_workout(workout):
        is_valid = True
        # checking name length
        if len(workout['name']) < 2:
            flash("Name must contain at least 2 characters", "update_workout_error")
            is_valid = False
        
        query = "SELECT * FROM workouts WHERE name = %(name)s"
        results = connectToMySQL(Workout.db).query_db(query, workout)
        data = {
            "id": workout['id']
        }
        my_workouts = Workout.get_by_id(data)
        if my_workouts.name == workout['name']:
            pass
        elif len(results) >= 1:
            flash("Name is already in use", "update_workout_error")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO workouts (name, description, user_id, created_at, updated_at) VALUES ( %(name)s, %(description)s, %(user_id)s, NOW(), NOW() );"
        return connectToMySQL(Workout.db).query_db(query, data)
    
    @classmethod
    def delete_by_id(cls,data):
        query = "DELETE FROM workouts WHERE id = %(id)s"
        return connectToMySQL(Workout.db).query_db(query, data)

    @classmethod
    def update(cls,data):
        query = "UPDATE workouts SET name=%(name)s, description=%(description)s, user_id=%(user_id)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(Workout.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM workouts;"
        results = connectToMySQL(Workout.db).query_db(query)
        workouts = []
        for workout in results:
            workouts.append( cls(workout))
        return workouts
    
    @classmethod
    def get_all_workouts_by_user_id(cls, data):
        query = "SELECT * FROM workouts WHERE user_id = %(id)s;"
        results = connectToMySQL(Workout.db).query_db(query, data)
        workouts = []
        for workout in results:
            workouts.append( cls(workout))
        return workouts

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM workouts WHERE id = %(id)s;"
        results = connectToMySQL(Workout.db).query_db(query, data)
        return cls(results[0])
    
    