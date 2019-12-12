
#import packages from Flask Lib
from flask import Flask, render_template, request, session, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Page
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
        booking_agent_id = request.form['agent id']

        if password != password_confirmation:                             
            flash("Password must match")
            return redirect(url_for('agent_register'))

        pw_hash = hashlib.md5(password.encode()) 

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
            cursor.execute(ins.format(email, pw_hash.hexdigest(), booking_agent_id))
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

        pw_hash = hashlib.md5(password.encode()) 

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
                email, name, pw_hash.hexdigest(),
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
            return render_template('home.html')
            #return redirect(url_for('home'))
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

        pw_hash = hashlib.md5(password.encode()) 

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
                pw_hash.hexdigest(),
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

@app.route('/s_repdates')
def s_repdates():
    return render_template('s_repdates.html')

@app.route('/s_repdatesAuth', methods = ['GET', 'POST'])
def s_repdatesAuth():
    try:
        usertype = session['type']
        if usertype == "staff":
            start = request.form['start']
            end = request.form['end']
            cursor = conn.cursor()
            query = 'SELECT count(ticket_id) as num FROM purchases WHERE purchase_date BETWEEN %s AND %s'
            cursor.execute(query, (start, end))
            data = cursor.fetchall()
            cursor.close()
            error = None
            if(data):
                cursor = conn.cursor()
                query = 'SELECT month(purchase_date) as month, count(ticket_id) as num FROM purchases WHERE purchase_date BETWEEN %s AND %s GROUP BY month ORDER BY month'
                cursor.execute(query, (start, end))
                bardata = cursor.fetchall()
                cursor.close()
                xbar = []
                ybar = []
                for dic in bardata:
                    xbar.append(dic['month'])
                    ybar.append(int(dic['num']))
                bar = Bar('View report in a for this time range')
                bar.add('Number of tickets', xbar, ybar)
                return render_template('s_repdates.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
            else:
                error = "No ticket available."
                return render_template('s_repdates.html', error = error)
        else:
            return render_template('error.html')
    except KeyError:
        return render_template('error.html')

@app.route('/s_repyr')
def s_repyr():
    try:
        usertype = session['type']
        if usertype == "staff":
            cursor = conn.cursor()
            query = 'SELECT count(ticket_id) as num FROM purchases WHERE purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()'
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            error = None
            if(data):
                cursor = conn.cursor()
                query = 'SELECT month(purchase_date) as month, count(ticket_id) as num FROM purchases WHERE purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE() GROUP BY month ORDER BY month'
                cursor.execute(query)
                bardata = cursor.fetchall()
                cursor.close()
                xbar = []
                ybar = []
                for dic in bardata:
                    xbar.append(dic['month'])
                    ybar.append(int(dic['num']))
                bar = Bar('View report of last year')
                bar.add('Number of tickets', xbar, ybar)
                return render_template('s_repyr.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
            else:
                error = "No ticket available."
                return render_template('s_repyr.html', error = error)
        else:
            return render_template('error.html')
    except KeyError:
        return render_template('error.html')

@app.route('/s_rmon')
def s_rmon():
    try:
        usertype = session['type']
        if usertype == "staff":
            cursor = conn.cursor()
            query = 'SELECT count(ticket_id) as num FROM purchases WHERE purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE()'
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            error = None
            if(data):
                return render_template('s_rmon.html', post = data)
            else:
                error = "No ticket available."
                return render_template('s_rmon.html', error = error)
        else:
            return render_template('error.html')
    except KeyError:
        return render_template('error.html')
@app.route('/s_comp')
def s_comp():
    try:
        usertype = session['type']
        if usertype == "staff":
            return render_template('revenue.html')
        else:
            return render_template('error.html')
    except KeyError:
        return render_template('error.html')

@app.route('/s_compyr')
def s_compyr():
    try:
        usertype = session['type']
        if usertype == "staff":
            cursor = conn.cursor()
            query = 'SELECT sum(price) FROM purchases, ticket, flight WHERE purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent_id is null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE())'
            cursor.execute(query)
            direct = cursor.fetchone()
            cursor.close()
            cursor = conn.cursor()
            query = 'SELECT sum(price) FROM purchases, ticket, flight WHERE purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent_id is not null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE())'
            cursor.execute(query)
            indirect = cursor.fetchone()
            cursor.close()
            xpie = ['direct to customer', '3rd party']
            ypie = []
            print(direct, indirect)
            for key in direct:
                if direct[key] == None:
                    ypie.append(0)
                else:
                    ypie.append(int(direct[key]))
            for key in indirect:
                if indirect[key] == None:
                    ypie.append(0)
                else:
                    ypie.append(int(indirect[key]))
            pie = Pie('Revenue in last year')
            pie.add('',xpie,ypie,is_label_show = True)
            return render_template('s_compyr.html', myechart = pie.render_embed(), host = REMOTE_HOST, script_list=pie.get_js_dependencies())
        else:
            return render_template('error.html')
    except KeyError:
        return render_template('error.html')

@app.route('/s_compmon')
def s_compmon():
    try:
        usertype = session['type']
        if usertype == "staff":
            cursor = conn.cursor()
            query = 'SELECT sum(price) FROM purchases, ticket, flight WHERE purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent_id is null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE())'
            cursor.execute(query)
            direct = cursor.fetchone()
            cursor.close()
            cursor = conn.cursor()
            query = 'SELECT sum(price) FROM purchases, ticket, flight WHERE purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent_id is not null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE())'
            cursor.execute(query)
            indirect = cursor.fetchone()
            cursor.close()
            xpie = ['direct to customer', '3rd party']
            ypie = []
            for key in direct:
                if direct[key] == None:
                    ypie.append(0)
                else:
                    ypie.append(int(direct[key]))
            for key in indirect:
                if indirect[key] == None:
                    ypie.append(0)
                else:
                    ypie.append(int(indirect[key]))
            pie = Pie('Revenue in last month')
            pie.add('',xpie,ypie,is_label_show = True)
            return render_template('s_compmon.html', myechart = pie.render_embed(), host = REMOTE_HOST, script_list=pie.get_js_dependencies())
        else:
            return render_template('error.html')
    except KeyError:
        return render_template('error.html')

@app.route('/revenue', methods=['GET','POST'])
def revenue():
    if (session['type'] == 'staff'):
        return render_template('staff/revenue.html')
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

        return render_template('staff/report.html', data=data)
        
    error = 'Staff does not exist'
    return redirect(url_for('login', error=error))

@app.route('/revenue', methods=['GET','POST'])
def revenueR():
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
@app.route('/c_viewflights')
def c_viewflights():
    if (session['type'] == 'customer'):
        cursor = conn.cursor()
        query = 'SELECT airline_name, flight_num, ticket_id, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND status = "Upcoming"'
        cursor.execute(query, (session['email']))
        data = cursor.fetchall()
        cursor.close()
        error = None
        if (data):
            return render_template('c_viewflights.html', post = data)
        else:
            error = "You do not have any flight scheduled right now."
            return render_template('c_viewflights.html', error = error)
    else:
        return render_template('error.html')
   

@app.route('/c_search')
def c_search():
   if session['type'] == "customer":
          return render_template('c_search.html')
   else:
          return render_template('error.html')
       
   return render_template('error.html')


@app.route('/c_searchAuth', methods = ['GET','POST'])
def c_Auth():
       
   if session['type'] == "customer":
          source = request.form['source']
          destination = request.form['destination']
          date = request.form['date']
          cursor = conn.cursor()
          query = "SELECT flight.* FROM flight, airport as A1, airport as A2 WHERE departure_airport = A1.airport_name and arrival_airport = A2.airport_name and status = 'Upcoming' and (departure_airport = %s or A1.airport_city = %s) and (arrival_airport = %s or A2.airport_city = %s) and date(departure_time) = %s"
          cursor.execute(query, (source, source, destination, destination, date))
          data = cursor.fetchall()
          cursor.close()
          error = None
          if (data):
            return render_template('c_purchase.html', post = data)
          else:
            error = "Flight does not exist"
            return render_template("c_search.html", error = error)
   else:
        return render_template('error.html')
       
   return render_template('error.html')

@app.route('/c_purchase')
def c_purchase():
       
   usertype = session['type']
   if usertype == "customer":
        return render_template('c_purchase.html')
   else:
        return render_template('error.html')
       
   return render_template('error.html')


@app.route('/c_buyAuth', methods = ['GET', 'POST'])
def c_buyAuth():
    username = session['email']
    usertype = session['type']
    if (usertype == "customer"):
        airline_name = request.form['airline']
        flight_num = request.form['flight_num']
        cursor = conn.cursor()
        query = 'SELECT ticket_id FROM ticket WHERE airline_name = %s and flight_num = %s'
        cursor.execute(query, (airline_name, flight_num))
        data = cursor.fetchone()
        print(data)
        cursor.close()
        error = None
        if(data):
            ticket_id = data['ticket_id']
            cursor = conn.cursor()
            query = 'INSERT INTO purchases values (%s, %s, null, CURRENT_DATE())'
            cursor.execute(query, (ticket_id, username))
            conn.commit()
            cursor.close()
            return render_template('home.html', post = "Purchase successful!")
        else:
            error = "No tickets available."
            return render_template('c_purchase.html', error = error)
    else:
        return render_template('error.html')


@app.route('/c_tracker')
def c_tracker():

   usertype = session['type']
   if usertype == "customer":
          cursor = conn.cursor()
          query = 'SELECT sum(price) as sum FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE())'
          cursor.execute(query, session['email'])
          data = cursor.fetchall()
          cursor.close()
          error = None
          print(data)
          if (data):
            cursor = conn.cursor()
            query = 'SELECT month(purchase_date) as month, sum(price) as mon FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 6 MONTH) AND CURRENT_DATE()) GROUP BY month ORDER BY month'
            cursor.execute(query, (session['email']))
            bardata = cursor.fetchall()
            cursor.close()
            print(bardata)
            bar = Bar('Track my Spending within 6 months')
            xbar = []
            ybar =[]
            for dic in bardata:
                xbar.append(dic['month'])
                ybar.append(int(dic['mon']))
            print(xbar,ybar)
            bar.add('money spent',xbar,ybar)
            return render_template('c_tracker.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
          else:
            error = "You did not purchase any tickets."
            return render_template('c_tracker.html', error = error)
   else:
          return render_template('error.html')

@app.route('/c_details')
def c_details():
       return render_template('c_details.html')

@app.route('/c_detailsAuth', methods = ['GET', 'POST'])
def c_detailsAuth():
   username = session['email']
   usertype = session['type']
   if usertype == "customer":
          date_start = request.form["date start"]
          date_end = request.form["date end"]
          cursor = conn.cursor()
          query = 'SELECT sum(price) as sum FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN %s AND %s)'
          cursor.execute(query, (username, date_start, date_end))
          data = cursor.fetchall()
          cursor.close()
          error = None
          if (data):
            cursor = conn.cursor()
            query = 'SELECT month(purchase_date) as month, sum(price) as mon FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN %s AND %s) GROUP BY month ORDER BY month'
            cursor.execute(query, (username, date_start, date_end))
            bardata = cursor.fetchall()
            cursor.close()
            bar = Bar('Track my Spending during the follow dates:')
            xbar = []
            ybar =[]
            for dic in bardata:
                xbar.append(dic['month'])
                ybar.append(int(dic['mon']))
                bar.add('money',xbar,ybar)
            return render_template('c_details.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
          else:
            error = "You have not purchased a ticket."
            return render_template('c_details.html', error = error)
   else:
          return render_template('error.html')

# ----------------------------------------------
# AGENT
@app.route('/a_view')
def a_view():
	
		username = session['email']
		usertype = session['type']
		if usertype == "agent":
			cursor = conn.cursor()
			query = 'SELECT customer_email, airline_name, flight_num, ticket_id, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id FROM flight natural join ticket natural join purchases natural join booking_agent WHERE email = %s AND status = "upcoming"'
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				return render_template('a_view.html', post = data)
			else:
				error = "No flights purchased for customers."
				return render_template('a_view.html', error = error)
		else:
			return render_template('error.html')
	
		return render_template('error.html')

@app.route('/a_search')
def a_search():
	
		usertype = session['type']
		if usertype == "agent":
			return render_template('a_search.html')
		else:
			return render_template('error.html')
	
		return render_template('error.html')

@app.route('/a_searchAuth', methods = ['GET','POST'])
def a_searchAuth():
	
		usertype = session['type']
		if usertype == "agent":
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
				return render_template('a_purchase.html', post = data)
			else:
				error = "Flight does not exist"
				return render_template("a_search.html", error = error)
		else:
			return render_template('error.html')
	
		return render_template('error.html')

@app.route('/a_purchase')
def a_purchase():
	
		usertype = session['type']
		if usertype == "agent":
			return render_template('a_purchase.html')
		else:
			return render_template('error.html')
	
		return render_template('error.html')
	
# ******** LOOK BACK **********
@app.route('/a_purchaseAuth', methods = ['GET', 'POST'])
def a_purchaseAuth():
	
		usertype = session['type']
		if usertype == "agent":
			airline_name = request.form['airline name']
			flight_num = request.form['flight number']
			cursor = conn.cursor()
			query = 'SELECT ticket_id FROM ticket WHERE airline_name = %s and flight_num = %s and ticket_id not in (SELECT ticket_id from purchases)'
			cursor.execute(query, (airline_name, flight_num))
			data = cursor.fetchone()
			cursor.close()
			error = None
			if(data):
				return render_template('a_success.html', post = data)
			else:
				error = "No tickets left"
				return render_template('a_purchase.html', error = error)
		else:
			return render_template('error.html')
	
		return render_template('error.html')

@app.route('/a_success')
def a_buy():
	
		usertype = session['type']
		if usertype == "agent":
			return render_template('a_success.html')
		else:
			return render_template('error.html')
	
		return render_template('error.html')

@app.route('/a_successAuth', methods = ['GET', 'POST'])
def a_successAuth():
	
		username = session['email']
		usertype = session['type']
		if usertype == "agent":
			cursor = conn.cursor()
			query = 'SELECT booking_agent_id FROM booking_agent WHERE email = %s'
			cursor.execute(query, (username))
			data = cursor.fetchone()
			cursor.close()
			booking_agent_id = data['booking_agent_id']
			ticket_id = request.form['ticket id']
			customer = request.form['customer']
			cursor = conn.cursor()
			query = 'INSERT INTO purchases values (%s, %s, %s, CURRENT_DATE())'
			cursor.execute(query, (ticket_id, customer, booking_agent_id))
			conn.commit()
			cursor.close()
			return render_template('\.html', post = "Successful!")
		else:
			return render_template('error.html')
	
		return render_template('error.html')

@app.route('/a_com')
def a_commission():
	
		username = session['email']
		usertype = session['type']
		if usertype == "agent":
			cursor = conn.cursor()
			query = "SELECT 0.1 * sum(price) as Total, count(ticket_id) as Amount, 0.1 * sum(price)/count(ticket_id) as Average FROM purchases natural join ticket natural join flight natural join booking_agent WHERE email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE())"
			cursor.execute(query, (username))
			data = cursor.fetchone()
			conn.commit()
			cursor.close()
			error = None
			if(data):
				return render_template('a_com.html', post = data)
			else:
				error = "No commission yet, try harder."
				return render_template('a_com.html', error = error)
		else:
			return render_template('error.html')
	
		return render_template('error.html')

@app.route('/a_comdetail')
def a_commissiondetail():
	
		usertype = session['type']
		if usertype == "agent":
			return render_template('a_comdetail.html')
		else:
			return render_template('error.html')
	
		return render_template('error.html')

# *************************
@app.route('/a_comdAuth', methods = ['GET', 'POST'])
def a_comdAuth():
	
    username = session['email']
    usertype = session['type']
    if usertype == "agent":
        start = request.form['start date']
        end = request.form['end date']
        cursor = conn.cursor()
        query = "SELECT 0.1 * sum(price) as Total, count(ticket_id) as Amount FROM purchases natural join ticket natural join flight natural join booking_agent WHERE email = %s AND (purchase_date BETWEEN %s AND %s)"
        cursor.execute(query, (username, start, end))
        data = cursor.fetchone()
        conn.commit()
        cursor.close()
        error = None
        if(data):
            return render_template('a_comdetail.html', post = data)
        else:
            error = "No commission yet. Try harder..."
            return render_template('a_comdetail.html', error = error)
    else:
        return render_template('error.html')

    return render_template('error.html')

@app.route('/a_best5c')
def a_top():
	
		usertype = session['type']
		if usertype == "agent":
			return render_template('a_best5c.html')
		else:
			return render_template('error.html')
	
		return render_template('error.html')

@app.route('/a_bestmonth')
def a_topmonth():
	
		username = session['email']
		usertype = session['type']
		if usertype == "agent":
			cursor = conn.cursor()
			query = "SELECT customer_email as email, count(ticket_id) as num FROM purchases, booking_agent WHERE purchases.booking_agent_id = booking_agent.booking_agent_id AND email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 6 MONTH) AND CURRENT_DATE())  GROUP BY customer_email ORDER BY count(ticket_id) DESC LIMIT 5"
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				bar = Bar('View top Customers in the past 6 months')
				xbar = []
				ybar =[]
				for dic in data:
					xbar.append(dic['email'])
					ybar.append(int(dic['num']))
				bar.add('ticket number',xbar,ybar)
				return render_template('a_bestmonth.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
			else:
				error = "No customer data available."
				return render_template('a_bestmonth.html', error = error)
		else:
			return render_template('error.html')
	
		return render_template('error.html')

@app.route('/a_bestyear')
def a_topyear():
	
		username = session['email']
		usertype = session['type']
		if usertype == "agent":
			cursor = conn.cursor()
			query = "SELECT customer_email as email, sum(price) * 0.1 as commission FROM purchases, booking_agent, flight, ticket WHERE purchases.booking_agent_id = booking_agent.booking_agent_id AND ticket.ticket_id = purchases.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) GROUP BY customer_email ORDER BY sum(price) * 0.1 DESC LIMIT 5"
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			if (data):
				bar = Bar('View top Customers in the last year')
				xbar = []
				ybar =[]
				for dic in data:
					xbar.append(dic['email'])
					ybar.append(int(dic['commission']))
				bar.add('commission',xbar,ybar)
				return render_template('a_bestyear.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
			else:
				error = "No customer data available"
				return render_template('a_bestyear.html', error = error)
		else:
			return render_template('error.html')
	
		return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
