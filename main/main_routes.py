from flask import Blueprint, render_template

main = Blueprint('main', __name__,
                     template_folder='templates',
                     static_folder='static')

@main.route('/')
def home():
    return render_template('home.html')
