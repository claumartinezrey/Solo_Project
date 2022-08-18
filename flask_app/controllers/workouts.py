from crypt import methods
from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movement import Movement
from flask_app.models.workout import Workout
from flask_app.models.movement_completed import Movement_Completed
from flask_app.models.workout_completed import Workout_Completed

@app.route('/workouts')
def view_all_workouts():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    user = User.get_by_id(user_data)
    workouts = Workout.get_all_workouts_by_user_id(user_data)
    return render_template("my_workouts.html", user=user, workouts=workouts)


@app.route('/workouts/save', methods=['POST'])
def add_workout():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workout.validate_workout(request.form):
        return redirect('/workouts')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "user_id": session['user_id']
    }
    Workout.save(data)
    return redirect('/workouts')


@app.route('/workouts/<int:workout_id>/view')
def view_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    workout_data1 = {
        "workout_id": workout_id
    }
    workout_data2 = {
        "id": workout_id
    }
    user = User.get_by_id(user_data)
    workout = Workout.get_by_id(workout_data2)
    movements_completed = Movement_Completed.get_all_movements_by_workout_id(workout_data1)
    
    all_movements = Movement.get_all_movements_by_user_id(user_data)
    return render_template("view_workout.html", user=user, workout=workout, movements_completed=movements_completed, all_movements=all_movements)

@app.route('/workouts/<int:workout_id>/delete')
def delete_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": workout_id
    }
    Workout.delete_by_id(data)
    return redirect('/workouts')


@app.route('/workouts/<int:workout_id>/update', methods=['POST'])
def update_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workout.validate_updated_workout(request.form):
        return redirect(url_for('view_workout', workout_id=workout_id))
    data = {
        "id": request.form['id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "user_id": session['user_id']
    }
    Workout.update(data)
    return redirect(url_for('view_workout', workout_id=workout_id))

@app.route('/workouts/<int:workout_id>/add_movements')
def add_movements_to_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    workout_data = {
        'id': workout_id
    }
    movements_completed_data = {
        'workout_id': workout_id
    }
    workout = Workout.get_by_id(workout_data)
    all_movements = Movement.get_all()
    movements_completed = Movement_Completed.get_all_movements_by_workout_id(movements_completed_data)
    return render_template("add_movements_to_workout.html", workout=workout, all_movements=all_movements, movements_completed=movements_completed)


@app.route('/workouts/<int:workout_id>/add_movements/save', methods=['POST'])
def add_movements_to_workout_save(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Movement_Completed.validate_movement_completed(request.form):
        print("you passed the validation")
        return redirect(url_for('view_workout', workout_id=workout_id))
    if (request.form['reps'] == "reps"):
        reps = True
        data1 = {
            "name": request.form['name'],
            "reps": reps,
            "reps_amount": request.form['reps_amount'],
            "minutes": 0,
            "seconds": 0,
            "user_id": session['user_id'],
            "workout_id": request.form['workout_id'],
        }
        Movement_Completed.save(data1)
    else:
        reps = False
        data2 = {
            "name": request.form['name'],
            "reps": reps,
            "reps_amount": 0,
            "minutes": request.form['minutes'],
            "seconds": request.form['seconds'],
            "user_id": session['user_id'],
            "workout_id": request.form['workout_id'],
        }
        Movement_Completed.save(data2)
    return redirect(url_for('add_movements_to_workout', workout_id=workout_id))

@app.route('/movements_completed/<int:workout_id>/<int:movement_id>/delete')
def delete_movement_completed(workout_id, movement_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": movement_id
    }
    Movement_Completed.delete_by_id(data)
    return redirect(url_for('add_movements_to_workout', workout_id=workout_id))

