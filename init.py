# import packages from Flask Lib
from flask import Flask, render_template, request, session, url_for, redirect, flash
import random

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'some key that you will never guess'

from main import main_routes
app.register_blueprint(main_routes.main)

from auth import auth_routes
app.register_blueprint(auth_routes.auth)

from staff import staff_routes
app.register_blueprint(staff_routes.staff)
                
if __name__ == '__main__':
    app.run(debug=True)
