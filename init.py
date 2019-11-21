# import packages from Flask Lib
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import random

# Initialize Flask app
app = Flask(__name__)

conn = pymysql.connect(host='localhost',
                       user='root',
                       port=8889,
                       password='root',
                       db='airport_proj',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
@app.route('/home')
def start():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/customer_register')
def customer_register():
    return render_template('c_register.html')


@app.route('/agent_register')
def agent_register():
    return render_template('a_register.html')


@app.route('/staff_register')
def staff_register():
    return render_template('s_register.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/status')
def status():
    return render_template('status.html')

#app.secret_key("some key you will never guess")


if __name__ == '__main__':
    app.run(debug=True)
