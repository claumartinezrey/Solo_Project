from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re


class Movement_Completed:
    db = "workout_routines"
    def __init__(self, data):
        self.id = data['id']

        self.name = data['name']
        self.reps = data['reps']
        self.reps_amount = data['reps_amount']
        self.minutes = data['minutes']
        self.seconds = data['seconds']

        self.user_id = data['user_id']
        self.workout_id = data['workout_id']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # VALIDATIONS TO BE ENTERED HERE
    @staticmethod
    def validate_movement_completed(movement):
        print("you are in the validation")
        is_valid = True
        # checking name length
        if (movement['name'] == '-'):
            flash("You must select an exercise", "new_movement_completed_error")
            is_valid = False

        if ( movement['reps'] == '-'):
            flash("You must select By Reps or By Time", "new_movement_completed_error")
            is_valid = False
        
        if (movement['reps'] is False):
            if (movement['minutes'] < 1):
                if (movement['seconds'] < 1):
                    flash("You must enter a time", "new_movement_completed_error")
                    is_valid = False
        else:
            if (movement['reps_amount'] is None):
                    flash("You must enter a number of reps", "new_movement_completed_error")
                    is_valid = False
        return is_valid


    @classmethod
    def save(cls, data):
        query = "INSERT INTO movements_completed (name, reps, reps_amount, minutes, seconds, user_id, workout_id, created_at, updated_at) VALUES (%(name)s, %(reps)s, %(reps_amount)s, %(minutes)s, %(seconds)s, %(user_id)s, %(workout_id)s,  NOW(), NOW() );"
        return connectToMySQL(Movement_Completed.db).query_db(query, data)
    
    @classmethod
    def delete_by_id(cls,data):
        query = "DELETE FROM movements_completed WHERE id = %(id)s"
        return connectToMySQL(Movement_Completed.db).query_db(query, data)

    @classmethod
    def update(cls,data):
        pass

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM movements_completed;"
        results = connectToMySQL(Movement_Completed.db).query_db(query)
        movements = []
        for movement in results:
            movements.append( cls(movement))
        return movements
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM movements_completed WHERE id = %(id)s;"
        results = connectToMySQL(Movement_Completed.db).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_all_movements_by_workout_id(cls, data):
        query = "SELECT * FROM movements_completed WHERE workout_id = %(workout_id)s;"
        results = connectToMySQL(Movement_Completed.db).query_db(query, data)
        movements_completed = []
        for movement in results:
            movements_completed.append( cls(movement))
        return movements_completed