from flask import Blueprint, render_template
from flask import current_app as app

# Set up a Blueprint
main = Blueprint('main', __name__,
                     template_folder='templates',
                     static_folder='static')

@main.route('/')
def test():
    return render_template('test.html')

@main.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@main.route('/info')
def info():
    return render_template('info.html')

@main.route('/search')
def search():
    return render_template('search.html')

@main.route('/status')
def status():
    return render_template('status.html')
