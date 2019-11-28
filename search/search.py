from flask import Blueprint, render_template

search = Blueprint('search', __name__,
                     template_folder='templates',
                     static_folder='static')

import sys
sys.path.append("airline_proj")
from database import conn

@search.route('/search-flight', methods=['GET','POST'])
def flight():

    return render_template('info.html')


@search.route('/search-status', methods=['GET','POST'])
def status():
    return render_template('info.html')
