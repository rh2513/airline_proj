# import packages from Flask Lib
from flask import Flask, render_template, request, session, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

# from pyecharts import Bar
# from pyecharts import Pie
# from pyecharts import Page
import random

import pymysql.cursors

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

conn = pymysql.connect(host='localhost',
                user='root',
                port=8889,
                password='root',
                db='airport_proj',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'some key that you will never guess'


@app.route('/')
def home():
    cursor = conn.cursor()
    query = "SELECT * FROM flight "
    cursor.execute(query.format())
    data = cursor.fetchall()
    cursor.close()

    return render_template('home.html', data=data)

# ---------------------------------------------------------------------
# AUTHENTICATION
@app.route('/register')
def register():
    return render_template('register/register.html')


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/agent-register', methods=['GET', 'POST'])
def agent_register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form['password confirmation']
        booking_agent_id = request.form['booking agent id']

        if password != password_confirmation:
            flash("Password must match")
            return redirect(url_for('agent_register'))

        pw_hash = hashlib.md5(password.encode().hexdiges()) 

        cursor = conn.cursor()
        query = "SELECT * FROM booking_agent WHERE email = \'{}\'"
        cursor.execute(query.format(email))
        data = cursor.fetchone()
        error = None

        if(data):
            error = "This user already exists"
            return render_template('register/agent_register.html', error=error)
        else:
            ins = "INSERT INTO booking_agent VALUES(\'{}\', \'{}\', \'{}\')"
            cursor.execute(ins.format(email, pw_hash, booking_agent_id))
            conn.commit()
            cursor.close()
            return redirect(url_for('login'))
    else:
        return render_template('register/agent_register.html')


@app.route('/agent-login', methods=['POST'])
def agent_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = hashlib.md5(password.encode()) 
    
        cursor = conn.cursor()
        query = "SELECT * FROM booking_agent WHERE email = \'{}\' and password = \'{}\' "
        cursor.execute(query.format(email, result.hexdigest()))
        data = cursor.fetchone()
        cursor.close()
        error = None

        if(data):
            session['email'] = email
            session['type'] = 'agent'
            return redirect(url_for('home'))
        else:
            error = 'Invalid login or username'
            return redirect(url_for('login', error=error))

    return render_template('login.html')

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

        pw_hash = hashlib.md5(password.encode().hexdigest()) 

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
                email, name, pw_hash,
                building_number, street, city, state,
                phone_number,
                passport_number, passport_expiration, passport_country,
                date_of_birth))
            conn.commit()
            cursor.close()
            return redirect(url_for('login'))
    else:
        return render_template('register/customer_register.html')


@app.route('/customer-login', methods=['POST'])
def customer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = hashlib.md5(password.encode()) 

        cursor = conn.cursor()
        query = "SELECT * FROM customer WHERE email = \'{}\' and password = \'{}\'"
        cursor.execute(query.format(email, result.hexdigest()))
        data = cursor.fetchone()
        cursor.close()
        error = None

        if(data):
            session['email'] = email
            session['type'] = 'customer'
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
            return redirect(url_for('staff-register'))

        pw_hash = hashlib.md5(password.encode().hexdigest()) 

        cursor = conn.cursor()
        query = "SELECT * FROM airline_staff WHERE username = \'{}\'"
        cursor.execute(query.format(username))
        data = cursor.fetchone()
        error = None

        if(data):
            error = "This user already exists"
            return redirect(url_for('staff_register', error=error))
        else:
            ins = "INSERT INTO airline_staff VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
            cursor.execute(ins.format(
               username,
               pw_hash,
               first_name, last_name,
               date_of_birth,
               airline_name))
            conn.commit()
            cursor.close()
            return redirect(url_for('login'))

    return render_template('register/staff_register.html')


@app.route('/staff-login', methods=['POST'])
def staff_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = hashlib.md5(password.encode()) 

        cursor = conn.cursor()
        query = "SELECT * FROM airline_staff WHERE username = \'{}\' and password = \'{}\'"
        cursor.execute(query.format(username, result.hexdigest()))
        data = cursor.fetchone()
        cursor.close()
        error = None

        if(data):
            session['email'] = username
            session['type'] = 'staff'
            session['airline'] = data['airline_name']
            return redirect(url_for('home'))
        else:
            error = 'Invalid login or username'
            return redirect(url_for('login', error=error))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email')
    session.pop('type')
    return redirect('/')

# ---------------------------------------------------------------------
# SEARCH
@app.route('/search-flight', methods=['POST'])
def searchFlight():
    cursor = conn.cursor()
    query = "SELECT * FROM flight "
    cursor.execute(query.format())
    data = cursor.fetchall()
    cursor.close()

    filter = []
    for d in data:
        add = True
        if (request.form['flight_num'] not in str(d['flight_num']) and request.form['flight_num'] != ''):
            add = False
        # if (str(request.form['departure_time']) not in str(d['departure_time']) and request.form['departure_time'] != ''):
        #     add = False
        # if (str(request.form['arrival_time']) != str(d['arrival_time']) and request.form['arrival_time'] != ''):
        #     add = False
        if (request.form['departure_airport'] not in d['departure_airport'] and request.form['departure_airport'] != ''):
            add = False
        if (request.form['arrival_airport'] not in d['arrival_airport'] and request.form['arrival_airport'] != ''):
            add = False
        if (request.form['status'] not in d['status'] and request.form['status'] != ''):
            add = False
        if (add == True):
            filter.append(d)

    return render_template('home.html', data=filter)

# ---------------------------------------------------------------------
# STAFF

@app.route('/my-flight', methods=['GET'])
def getMyFlight():
    if (session['type'] == 'staff'):
        cursor = conn.cursor()
        query = "SELECT * FROM flight WHERE airline_name = \'{}\'"
        cursor.execute(query.format(session['airline']))
        data = cursor.fetchall()
        cursor.close()
        error = None
        if(data):
            return render_template('staff/my_flight.html', data=data)
        else:
            error = 'No current flights for this airline exist'
            return render_template('staff/my_flight.html', error=error)
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))


@app.route('/my-flight', methods=['POST'])
def postMyFlight():
    if (session['type'] == 'staff'):
        cursor = conn.cursor()
        query = "SELECT * FROM flight WHERE airline_name = \'{}\'"
        cursor.execute(query.format(session['airline'], request.form['departure_airport']))
        data = cursor.fetchall()
        cursor.close()
        error = None

        filter = []
        for d in data:
            add = True
            if (request.form['flight_num'] not in str(d['flight_num']) and request.form['flight_num'] != ''):
                add = False
            if (str(request.form['departure_time']) not in str(d['departure_time']) and request.form['departure_time'] != ''):
                add = False
            if (str(request.form['arrival_time']) != str(d['arrival_time']) and request.form['arrival_time'] != ''):
                add = False
            if (request.form['departure_airport'] not in d['departure_airport'] and request.form['departure_airport'] != ''):
                add = False
            if (request.form['arrival_airport'] not in d['arrival_airport'] and request.form['arrival_airport'] != ''):
                add = False
            if (add == True):
                filter.append(d)

        if(data):
            return render_template('staff/my_flight.html', data=filter)
        else:
            error = 'No current flights for this airline exist'
            return render_template('staff/my_flight.html', error=error)
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))


@app.route('/new-flight', methods=['GET','POST'])
def newFlight():
    if (session['type'] == 'staff'):
        if request.method == 'POST':
            airline_name = request.form['airline name']
            flight_num = request.form['flight num']
            departure_airport = request.form['departure airport']
            departure_time = request.form['departure time']
            arrival_airport = request.form['arrival airport']
            arrival_time = request.form['arrival time']
            price = request.form['price']
            status = request.form['status']
            airplane_id = request.form['airplane id']

            cursor = conn.cursor()
            query = "SELECT * FROM flight WHERE flight_num = \'{}\'"
            cursor.execute(query.format(flight_num))
            data = cursor.fetchone()
            cursor.close()
            error = None

            if(data):
                error = 'Invalid flight'
                return render_template('staff/create_flight.html', error=error)
            else:
                cursor = conn.cursor()
                ins = "INSERT INTO flight VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
                cursor.execute(ins.format(
                airline_name,
                flight_num,
                departure_airport, departure_time,
                arrival_airport, arrival_time,
                price,
                status,
                airplane_id))
                conn.commit()
                cursor.close()
                return redirect(url_for('home'))

        return render_template('staff/create_flight.html')
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/flight/<slug>')
def lookAtFlight(slug):
    if (session['type'] == 'staff'):
        cursor = conn.cursor()
        query = "SELECT * FROM flight WHERE flight_num = \'{}\'"
        cursor.execute(query.format(slug))
        data = cursor.fetchone()
        cursor.close()
        error = None
        if (data):
            return render_template('staff/individual_flight.html', data=data, staff="true")
        else:
            error = "FLIGHT DOES NOT EXIST"
            return render_template('staff/my_flight.html', error=error)
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/edit-flight/<slug>', methods=['GET','POST'])
def editFlight(slug):
    if (session['type'] == 'staff'):
        cursor = conn.cursor()
        query = "SELECT * FROM flight WHERE flight_num = \'{}\'"
        cursor.execute(query.format(slug))
        data = cursor.fetchone()
        cursor.close()
        error = None

        if (data):
            if request.method == 'POST':
                cursor = conn.cursor()
                query = "DELETE FROM flight WHERE flight_num = \'{}\'"
                cursor.execute(query.format(slug))
                cursor.close()

                airline_name = request.form['airline name']
                flight_num = request.form['flight num']
                departure_airport = request.form['departure airport']
                departure_time = request.form['departure time']
                arrival_airport = request.form['arrival airport']
                arrival_time = request.form['arrival time']
                price = request.form['price']
                status = request.form['status']
                airplane_id = request.form['airplane id']

                status = request.form['status']
                cursor = conn.cursor()
                query = "INSERT INTO flight VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
                cursor.execute(query.format(
                airline_name,
                flight_num,
                departure_airport, departure_time,
                arrival_airport, arrival_time,
                price,
                status,
                airplane_id))
                conn.commit()
                cursor.close()
                return redirect(url_for('lookAtFlight', slug=slug))

            return render_template('staff/edit_flight.html', data=data)

        error = "FLIGHT DOES NOT EXIST"
        return render_template('staff/edit_flight.html', error=error)
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/add-airplane', methods=['GET','POST'])
def addAirplane():
    if (session['type'] == 'staff'):
        if request.method == 'POST':
            airline_name = request.form['airline name']
            airplane_id = request.form['airplane id']
            seats = request.form['seats']

            cursor = conn.cursor()
            query = "SELECT * FROM airplane WHERE airplane_id = \'{}\'"
            cursor.execute(query.format(airplane_id))
            data = cursor.fetchone()
            cursor.close()
            error = None

            if(data):
                error = 'Invalid airplane'
                return redirect(url_for('add-airplane', error=error))
            else:
                cursor = conn.cursor()
                ins = "INSERT INTO airplane VALUES(\'{}\', \'{}\', \'{}\')"
                cursor.execute(ins.format(
                airline_name,
                airplane_id,
                seats))
                conn.commit()
                cursor.close()
                return redirect(url_for('home'))

        return render_template('staff/add_airplane.html')
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/add-airport', methods=['GET','POST'])
def addAirport():
    if (session['type'] == 'staff'):
        if request.method == 'POST':
            airport_name = request.form['airport name']
            airport_city = request.form['airport city']

            cursor = conn.cursor()
            query = "SELECT * FROM airport WHERE airport_name = \'{}\'"
            cursor.execute(query.format(airport_name))
            data = cursor.fetchone()
            cursor.close()
            error = None

            if(data):
                error = 'Invalid airport'
                return redirect(url_for('add-airport', error=error))
            else:
                cursor = conn.cursor()
                ins = "INSERT INTO airport VALUES(\'{}\', \'{}\')"
                cursor.execute(ins.format(
                airport_name,
                airport_city))
                conn.commit()
                cursor.close()
                return redirect(url_for('home'))

        return render_template('staff/add_airport.html')
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/booking-agent', methods=['GET'])
def bookingAgent():
    if (session['type'] == 'staff'):
        cursor = conn.cursor()
        query = "SELECT * FROM booking_agent"
        cursor.execute(query.format())
        data = cursor.fetchall()
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT booking_agent_id, count(booking_agent_id) AS num FROM purchases WHERE purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 30 MONTH) AND NOW() GROUP BY booking_agent_id ORDER BY num DESC LIMIT 5"
        cursor.execute(query.format())
        top5month = cursor.fetchall()
        cursor.close()

        print(top5month)
        cursor = conn.cursor()
        query = "SELECT booking_agent_id, count(booking_agent_id) AS num FROM purchases WHERE YEAR(purchase_date)= YEAR(CURRENT_DATE) or YEAR(purchase_date)= YEAR(CURRENT_DATE)-1 GROUP BY booking_agent_id ORDER BY num DESC LIMIT 5"
        cursor.execute(query.format())
        top5year = cursor.fetchall()
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT booking_agent_id, sum(price) as num FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id is not NULL GROUP BY booking_agent_id ORDER BY num DESC LIMIT 5"
        cursor.execute(query.format())
        top5commission = cursor.fetchall()
        cursor.close()

        return render_template('staff/booking_agent.html', agent_list=data, top5month=top5month, top5year=top5year, top5commission=top5commission)
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/customer', methods=['GET'])
def customer():
    if (session['type'] == 'staff'):
        cursor = conn.cursor()
        query = "SELECT * FROM customer"
        cursor.execute(query.format())
        data = cursor.fetchall()
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT customer_email, count(customer_email) AS num FROM purchases WHERE YEAR(purchase_date)= YEAR(CURRENT_DATE) or YEAR(purchase_date)= YEAR(CURRENT_DATE)-1 GROUP BY customer_email ORDER BY num DESC LIMIT 5"
        cursor.execute(query.format())
        customer = cursor.fetchall()
        cursor.close()

        return render_template('staff/customer.html', customer_list=data, topcustomer=customer)
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/customer-flight/<slug>', methods=['GET'])
def individualCustomer(slug):
    if (session['type'] == 'staff'):
        cursor = conn.cursor()
        query = "SELECT * FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE customer_email=\'{}\' AND airline_name=\'{}\'"
        cursor.execute(query.format(slug, session['airline']))
        customer = cursor.fetchall()
        cursor.close()
        return render_template('staff/individual_customer.html', customer=customer)
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/report', methods=['GET','POST'])
def report():
    if (session['type'] == 'staff'):
        cursor = conn.cursor()
        query = "SELECT count(*) FROM ticket"
        cursor.execute(query.format())
        data = cursor.fetchall()
        cursor.close()

        # filter = []
        # for d in data:
        #     add = True
        #     # range of dates
        #     if (request.form[''] not in d[''] and request.form[''] != ''):
        #         add = False
        #     if (request.form[''] not in d[''] and request.form[''] != ''):
        #         add = False
        #     if (request.form[''] not in d[''] and request.form[''] != ''):
        #         add = False
        #     if (request.form[''] not in d[''] and request.form[''] != ''):
        #         add = False
        #     if (add == True):
        #         filter.append(d)


        return render_template('staff/report.html', data=data)
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/revenue', methods=['GET','POST'])
def revenue():
    if (session['type'] == 'staff'):
        return render_template('staff/revenue.html')
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/top-destination', methods=['GET','POST'])
def topDestination():
    if (session['type'] == 'staff'):
        cursor = conn.cursor()
        query = "SELECT * FROM (SELECT count(arrival_airport) as airport, arrival_airport FROM flight GROUP BY (arrival_airport)) as destination ORDER BY airport DESC LIMIT 3"
        cursor.execute(query.format())
        data = cursor.fetchall()
        cursor.close()
        
        return render_template('staff/top_destination.html', data=data)
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

# --------------------------------------------------------------------
# CUSTOMER

@app.route('/customer_home')
def customer_home():
	try:
		usertype = session['type']
		if usertype == "customer":
			return render_template('c_home.html')
		else:
			return render_template('error.html')
	except KeyError:
		return render_template('error.html')

@app.route('/c_viewflights')
def c_view():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "customer":
			cursor = conn.cursor()
			query = 'SELECT airline_name, flight_num, ticket_id, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND status = "upcoming"'
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				return render_template('c_viewflights.html', post = data)
			else:
				error = "You do not have any flight right now. Go get some."
				return render_template('c_viewflights.html', error = error)
		else:
			return render_template('error.html')
	except KeyError:
		return render_template('error.html')

@app.route('/c_search')
def c_search():
	try:
		usertype = session['type']
		if usertype == "customer":
			return render_template('c_search.html')
		else:
			return render_template('error.html')
	except KeyError:
		return render_template('error.html')


@app.route('/c_searchAuth', methods = ['GET','POST'])
def c_searchAuth():
	try:
		usertype = session['type']
		if usertype == "customer":
			source = request.form['source']
			destination = request.form['destination']
			date = request.form['date']
			cursor = conn.cursor()
			query = "SELECT flight.* FROM flight, airport as T1, airport as T2 WHERE departure_airport = T1.airport_name and arrival_airport = T2.airport_name and status = 'upcoming' and (departure_airport = %s or T1.airport_city = %s) and (arrival_airport = %s or T2.airport_city = %s) and date(departure_time) = %s"
			cursor.execute(query, (source, source, destination, destination, date))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				return render_template('c_purchase.html', post = data)
			else:
				error = "No such flight"
				return render_template("c_search.html", error = error)
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')

@app.route('/c_purchase')
def c_purchase():
	try:
		usertype = session['type']
		if usertype == "customer":
			return render_template('c_purchase.html')
		else:
			return render_template('wrong.html')
	except KeyError:
		return render_template('wrong.html')


@app.route('/c_purchaseAuth', methods = ['GET', 'POST'])
def c_purchaseAuth():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "customer":
			airline_name = request.form['airline name']
			flight_num = request.form['flight number']
			cursor = conn.cursor()
			query = 'SELECT ticket_id FROM ticket WHERE airline_name = %s and flight_num = %s and ticket_id not in (SELECT ticket_id from purchases)'
			cursor.execute(query, (airline_name, flight_num))
			data = cursor.fetchone()
			cursor.close()
			error = None
			if(data):
				ticket_id = data['ticket_id']
				cursor = conn.cursor()
				query = 'INSERT INTO purchases values (%s, %s, null, CURRENT_DATE())'
				cursor.execute(query, (ticket_id, username))
				conn.commit()
				cursor.close()
				return render_template('c_home.html', post = "Purchase successful!")
			else:
				error = "No tickets available."
				return render_template('c_purchase.html', error = error)
		else:
			return render_template('error.html')
	except KeyError:
		return render_template('error.html')


# @app.route('/c_spending')
# def c_spending():
# 	try:
# 		username = session['value']
# 		usertype = session['type']
# 		if usertype == "Customer":
# 			cursor = conn.cursor()
# 			query = 'SELECT sum(price) as sum FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE())'
# 			cursor.execute(query, (username))
# 			data = cursor.fetchall()
# 			cursor.close()
# 			error = None
# 			print(data)
# 			if (data):
# 				cursor = conn.cursor()
# 				query = 'SELECT month(purchase_date) as month, sum(price) as money1 FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 6 MONTH) AND CURRENT_DATE()) GROUP BY month ORDER BY month'
# 				cursor.execute(query, (username))
# 				bardata = cursor.fetchall()
# 				cursor.close()
# 				print(bardata)
# 				bar = Bar('Track my Spending within 6 months')
# 				xbar = []
# 				ybar =[]
# 				for dic in bardata:
# 					xbar.append(dic['month'])
# 					ybar.append(int(dic['money1']))
# 				print(xbar,ybar)
# 				bar.add('money',xbar,ybar)
# 				return render_template('c_tracker.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
# 			else:
# 				error = "You have not get any ticket."
# 				return render_template('c_tracker.html', error = error)
# 		else:
# 			return render_template('error.html')
# 	except KeyError:
# 		return render_template('error.html')

@app.route('/c_details')
def c_details():
	return render_template('c_details.html')

# @app.route('/c_detailsAuth', methods = ['GET', 'POST'])
# def c_detailsAuth():
# 	try:
# 		username = session['value']
# 		usertype = session['type']
# 		if usertype == "Customer":
# 			date_start = request.form["date start"]
# 			date_end = request.form["date end"]
# 			cursor = conn.cursor()
# 			query = 'SELECT sum(price) as sum FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN %s AND %s)'
# 			cursor.execute(query, (username, date_start, date_end))
# 			data = cursor.fetchall()
# 			cursor.close()
# 			error = None
# 			if (data):
# 				cursor = conn.cursor()
# 				query = 'SELECT month(purchase_date) as month, sum(price) as money1 FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN %s AND %s) GROUP BY month ORDER BY month'
# 				cursor.execute(query, (username, date_start, date_end))
# 				bardata = cursor.fetchall()
# 				cursor.close()
# 				bar = Bar('Track my Spending in a range')
# 				xbar = []
# 				ybar =[]
# 				for dic in bardata:
# 					xbar.append(dic['month'])
# 					ybar.append(int(dic['money1']))
# 				bar.add('money',xbar,ybar)
# 				return render_template('c_details.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
# 			else:
# 				error = "You have not get any ticket."
# 				return render_template('c_details.html', error = error)
# 		else:
# 			return render_template('error.html')
# 	except KeyError:
# 		return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
