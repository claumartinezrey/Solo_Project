from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re


class Workout_Completed:
    db = "workout_routines"
    def __init__(self, data):
        self.id = data['id']
        self.day = data['day']
        self.workout_name = data['workout_name']
        self.completed = data['completed']
        self.user_id = data['user_id']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # VALIDATIONS TO BE ENTERED HERE

    @staticmethod
    def validate_workout_completed(workout):
        is_valid = True
        # checking name length
        if (workout['day']) == '-':
            flash("You must select a day", "new_workout_completed_error")
            is_valid = False
        
        if (workout['workout_name']) == '-':
            flash("You must select a workout", "new_workout_completed_error")
            is_valid = False
        data ={
            "id": session['user_id']
        }
        query = "SELECT workouts_completed.day FROM users LEFT JOIN workouts_completed ON users.id = workouts_completed.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(Workout_Completed.db).query_db(query, data)
        for result in results:
            if (workout['day'] == result['day']):
                flash("You must delete the workout you already have for that day to enter a new one", "new_workout_completed_error")
                is_valid = False
        return is_valid


    @classmethod
    def save(cls, data):
        query = "INSERT INTO workouts_completed (day, workout_name, completed, user_id, created_at, updated_at) VALUES ( %(day)s, %(workout_name)s, %(completed)s, %(user_id)s, NOW(), NOW() );"
        return connectToMySQL(Workout_Completed.db).query_db(query, data)

    @classmethod
    def delete_by_day(cls,data):
        query = "DELETE FROM workouts_completed WHERE day = %(day)s"
        return connectToMySQL(Workout_Completed.db).query_db(query, data)

    @classmethod
    def update(cls,data):
        pass

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM workouts_completed;"
        results = connectToMySQL(Workout_Completed.db).query_db(query)
        workouts = []
        for workout in results:
            workouts.append( cls(workout))
        return workouts
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM workouts_completed WHERE id = %(id)s;"
        results = connectToMySQL(Workout_Completed.db).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_all_by_user_id(cls, data):
        query = "SELECT * FROM workouts_completed WHERE user_id = %(id)s;"
        results = connectToMySQL(Workout_Completed.db).query_db(query, data)
        workouts = []
        for workout in results:
            workouts.append( cls(workout))
        return workouts
    
    @classmethod
    def get_by_name(cls, data):
        query = "SELECT * FROM workouts_completed WHERE name = %(name)s;"
        results = connectToMySQL(Workout_Completed.db).query_db(query, data)
        return cls(results[0])
    