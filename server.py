import py_compile
from flask_app.controllers import users
from flask_app.controllers import workouts
from flask_app.controllers import movements
from flask_app import app

if __name__ == "__main__":
    app.run(debug = True)
