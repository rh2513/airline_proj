from flask import Blueprint, Flask, render_template, request, session, url_for, redirect, flash
from flask import current_app as app

import sys
sys.path.append("airline_proj")
from database import conn

auth = Blueprint('auth', __name__,
                     template_folder='templates',
                     static_folder='static')

@auth.route('/register')
def register():
    return render_template('register/register.html')

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/agent-register', methods=['GET','POST'])
def agent_register():
    print("HI")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form['password confirmation']
        booking_agent_id = request.form['booking agent id']

        if password != password_confirmation:
            flash("Password must match")
            return redirect(url_for('main.agent_register'))
        if not len(password) >= 4:
            flash("Password length must be at least 4 characters")
            return redirect(url_for('main.agent_register'))

        cursor = conn.cursor()
        query = "SELECT * FROM booking_agent WHERE email = \'{}\'"
        cursor.execute(query.format(email))
        data = cursor.fetchone()
        error = None

        if(data):
            error = "This user already exists"
            return redirect(url_for('main.agent_register', error=error))
        else:
            ins = "INSERT INTO booking_agent VALUES(\'{}\', \'{}\', \'{}\')"
            cursor.execute(ins.format(email, password, booking_agent_id))
            conn.commit()
            cursor.close()
            return redirect(url_for('main.login'))
    else:
        return render_template('register/agent_register.html')

@auth.route('/agent-login', methods=['POST'])
def agent_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = conn.cursor()
        query = "SELECT * FROM booking_agent WHERE email = \'{}\' and password = \'{}\'"
        cursor.execute(query.format(email, password))
        data = cursor.fetchone()
        cursor.close()
        error = None

        if(data):
            session['email'] = email
            session['type'] = 'agent'
            return redirect(url_for('main.home'))
        else:
            error = 'Invalid login or username'
            return redirect(url_for('main.login', error=error))

    return render_template('login.html')

# CUSTOMER AUTHENTICATION (SIGNUP / LOGIN)
@auth.route('/customer-register', methods=['GET','POST'])
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
            return redirect(url_for('main.customer_register'))
        if not len(password) >= 4:
            flash("Password length must be at least 4 characters")
            return redirect(url_for('main.customer_register'))

        cursor = conn.cursor()
        query = "SELECT * FROM customer WHERE email = \'{}\'"
        cursor.execute(query.format(email))
        data = cursor.fetchone()
        error = None

        if(data):
            error = "This user already exists"
            return redirect(url_for('main.customer_register', error=error))
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
            return redirect(url_for('main.login'))
    else:
        print("HERE")
        return render_template('register/customer_register.html')

@auth.route('/customer-login', methods=['POST'])
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
            session['type'] = 'customer'
            return redirect(url_for('main.home'))
        else:
            error = 'Invalid login or username'
            return redirect(url_for('main.login', error=error))

    return render_template('login.html')

# STAFF AUTHENTICATION (SIGNUP / LOGIN)
@auth.route('/staff-register', methods=['GET','POST'])
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
            return redirect(url_for('main.staff-register'))
        if not len(password) >= 4:
            flash("Password length must be at least 4 characters")
            return redirect(url_for('main.staff-register'))

        cursor = conn.cursor()
        query = "SELECT * FROM airline_staff WHERE username = \'{}\'"
        cursor.execute(query.format(username))
        data = cursor.fetchone()
        error = None

        if(data):
            error = "This user already exists"
            return redirect(url_for('main.staff_register', error=error))
        else:
            ins = "INSERT INTO airline_staff VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
            cursor.execute(ins.format(
               username,
               password,
               first_name, last_name,
               date_of_birth,
               airline_name))
            conn.commit()
            cursor.close()
            return redirect(url_for('main.login'))

    return render_template('register/staff_register.html')

@auth.route('/staff-login', methods=['POST'])
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
            session['email'] = username
            session['type'] = 'staff'
            return redirect(url_for('main.home'))
        else:
            error = 'Invalid login or username'
            return redirect(url_for('login', error=error))

    return render_template('main.ogin.html')

@auth.route('/logout')
def logout():
    session.pop('email')
    return redirect('/')

