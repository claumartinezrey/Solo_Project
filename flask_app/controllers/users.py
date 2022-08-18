from crypt import methods
from shutil import move
from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt   
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movement import Movement
from flask_app.models.workout import Workout
from ..models.workout_completed import Workout_Completed
# from flask_app.models.sighting import Sighting


bcrypt = Bcrypt(app)

#route used to redirect to main page
@app.route('/')
def main():
    return redirect('/main')

#route used to display the screen for login and registration
@app.route('/main')
def main_page():
    return render_template("index.html")

#route used to process registration request
@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect("/main")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }
    User.save(data)
    user = User.get_by_email(data)
    session['user_id'] = user.id
    return redirect('/success')

#route used to process login request
@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid email/password", "login_error")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid email/password", "login_error")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/success')

#route used to display success screen with all sightings
@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    monday = ""
    tuesday = ""
    wednesday = ""
    thursday = ""
    friday = ""
    saturday = ""
    sunday = ""

    user = User.get_by_id(user_data)
    workouts_completed = Workout_Completed.get_all_by_user_id(user_data)
    for workout in workouts_completed:
        if workout.day == 'Monday':
            monday = workout.workout_name
        elif workout.day == 'Tuesday':
            tuesday = workout.workout_name
        elif workout.day == 'Wednesday':
            wednesday = workout.workout_name
        elif workout.day == 'Thursday':
            thursday = workout.workout_name
        elif workout.day == 'Friday':
            friday = workout.workout_name
        elif workout.day == 'Saturday':
            saturday = workout.workout_name
        elif workout.day == 'Sunday':
            sunday = workout.workout_name

    all_workouts = Workout.get_all_workouts_by_user_id(user_data)
    return render_template("home.html", user=user, all_workouts=all_workouts, monday=monday, tuesday=tuesday, wednesday=wednesday, thursday=thursday, friday=friday, saturday=saturday, sunday=sunday)

@app.route('/account')
def view_my_account():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    movement_data = {
        "user_id": session['user_id']
    }
    user = User.get_by_id(user_data)
    movements = Movement.get_all_movements_by_user_id(user_data)
    movements_sum = 0
    for movement in movements:
        movements_sum += 1
    workouts = Workout.get_all_workouts_by_user_id(user_data)
    workouts_sum = 0
    for workout in workouts:
        workouts_sum += 1
    return render_template('my_account.html', user=user, movements_sum=movements_sum, workouts_sum=workouts_sum)

@app.route('/account/edit')
def edit_my_account():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    user = User.get_by_id(user_data)
    return render_template('edit_account.html', user=user)

@app.route('/account/edit/save', methods=['POST'])
def save_edited_account():
    if not User.validate_user_edited(request.form):
        return redirect("/account/edit")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'id': request.form['id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }
    User.update_user_by_id(data)
    user = User.get_by_email(data)
    session['user_id'] = user.id
    return redirect('/account')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/success/add_workout_completed/save', methods=['POST'])
def add_workout_completed():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workout_Completed.validate_workout_completed(request.form):
        return redirect('/success')

    data = {
        "day": request.form['day'],
        "workout_name": request.form['workout_name'],
        "completed": request.form['completed'],
        "user_id": session['user_id'],
    }
    Workout_Completed.save(data)
    return redirect('/success')

@app.route('/success/workout_completed/<string:workout_day>/delete')
def delete_workout_completed(workout_day):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    data = {
        "day": workout_day
    }
    workouts_completed = Workout_Completed.get_all_by_user_id(user_data)
    for workout in workouts_completed:
        if workout.day == workout_day:
            print(" this is" + workout.day)
            Workout_Completed.delete_by_day(data)
    return redirect('/success')













