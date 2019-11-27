# import packages from Flask Lib
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import random

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'some key that you will never guess'

conn = pymysql.connect(host='localhost',
                       user='root',
                       port=8889,
                       password='root',
                       db='airport_proj',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def test():
    return render_template('test.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

# REGISTER
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/agent_register')
def agent_register():
    return render_template('agent_register.html')

# CUSTOMER AUTHENTICATION (SIGNUP / LOGIN)
@app.route('/customer-register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        street = request.form['street']
        building_number = request.form['building number']
        city = request.form['city']
        state = request.form['state']
        phone_number = request.form['phone number']
        passport_number = request.form['passport number']
        passport_expiration = request.form['passport expiration']
        passport_country = request.form['passport country']
        date_of_birth = request.form['date of birth']
        password = request.form['password']
        password_confirmation = request.form['password confirmation']

        if password != password_confirmation:
            flash("Password must match")
            return redirect(url_for('customer_register'))
        if not len(password) >= 4:
            flash("Password length must be at least 4 characters")
            return redirect(url_for('customer_register'))

        cursor = conn.cursor()
        query = "SELECT * FROM customer WHERE email = \'{}\'"
        cursor.execute(query.format(email))
        data = cursor.fetchone()
        error = None

        if(data):
            error = "This user already exists"
            return redirect(url_for('customer_register', error=error))
        else:
            ins = "INSERT INTO customer VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
            cursor.execute(ins.format(
                email, name, password,
                building_number, street, city, state,
                phone_number,
                passport_number, passport_expiration, passport_country,
                date_of_birth))
            conn.commit()
            cursor.close()
            flash("You are logged in")
            return redirect(url_for('home'))

    return render_template('customer_register.html')

@app.route('/customer-login', methods=['GET','POST'])
def customer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = conn.cursor()
        query = "SELECT * FROM customer WHERE email = \'{}\' and password = \'{}\'"
        cursor.execute(query.format(email, password))
        data = cursor.fetchone()
        cursor.close()
        error = None

        if(data):
            session['email'] = email
            return redirect(url_for('home'))
        else:
            error = 'Invalid login or username'
            return redirect(url_for('login', error=error))

    return render_template('login.html')


# STAFF AUTHENTICATION (SIGNUP / LOGIN)
@app.route('/staff-register', methods=['GET', 'POST'])
def staff_register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first name']
        last_name = request.form['last name']
        date_of_birth = request.form['date of birth']
        airline_name = request.form['airline name']
        password = request.form['password']
        password_confirmation = request.form['password confirmation']

        if password != password_confirmation:
            flash("Password must match")
            return redirect(url_for('customer_register'))
        if not len(password) >= 4:
            flash("Password length must be at least 4 characters")
            return redirect(url_for('customer_register'))

        cursor = conn.cursor()
        query = "SELECT * FROM airline_staff WHERE username = \'{}\'"
        cursor.execute(query.format(username))
        data = cursor.fetchone()
        error = None

        if(data):
            error = "This user already exists"
            return redirect(url_for('staff_register', error=error))
        else:
            ins = "INSERT INTO airline_staff VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
            cursor.execute(ins.format(
               username,
               password,
               first_name, last_name,
               date_of_birth,
               airline_name))
            conn.commit()
            cursor.close()
            flash("You are logged in")
            return redirect(url_for('home'))

    return render_template('staff_register.html')

@app.route('/staff-login', methods=['GET','POST'])
def staff_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor()
        query = "SELECT * FROM airline_staff WHERE username = \'{}\' and password = \'{}\'"
        cursor.execute(query.format(username, password))
        data = cursor.fetchone()
        cursor.close()
        error = None

        if(data):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid login or username'
            return redirect(url_for('login', error=error))

    return render_template('login.html')

@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/status')
def status():
    return render_template('status.html')


@app.route('/logout')
def logout():
    session.pop('email')
    return redirect('/')

# app.secret_key("secret")

if __name__ == '__main__':
    app.run(debug=True)
