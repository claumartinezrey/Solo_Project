from crypt import methods
from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movement import Movement
from flask_app.models.movement_completed import Movement_Completed
# from flask_app.models.sighting import Sighting


@app.route('/movements')
def view_all_movements():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    user = User.get_by_id(user_data)
    movements = Movement.get_all_movements_by_user_id(user_data)
    return render_template("my_movements.html", user=user, movements=movements)



@app.route('/movements/save', methods=['POST'])
def add_movement():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Movement.validate_movement(request.form):
        return redirect('/movements')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "user_id": session['user_id']
    }
    Movement.save(data)
    return redirect('/movements')

@app.route('/movements/<int:movement_id>/delete')
def delete_movement(movement_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": movement_id
    }
    Movement.delete_by_id(data)
    return redirect('/movements')


@app.route('/movements/<int:movement_id>/view')
def view_movement(movement_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": movement_id
    }
    movement = Movement.get_by_id(data)
    return render_template('view_movement.html', movement=movement)

@app.route('/movements/<int:movement_id>/update', methods=['POST'])
def update_movement(movement_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Movement.validate_updated_movement(request.form):
        return redirect(url_for('view_movement', movement_id=movement_id))
    data = {
        "id": request.form['id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "user_id": session['user_id']
    }
    Movement.update(data)
    return redirect(url_for('view_movement', movement_id=movement_id))

