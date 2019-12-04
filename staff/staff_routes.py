from flask import Blueprint, render_template, request, redirect, url_for

staff = Blueprint('staff', __name__,
                     template_folder='templates',
                     static_folder='static')

import sys
sys.path.append("airline_proj")
from database import conn

@staff.route('/my-flight', methods=['GET'])
def getMyFlight():     
    return render_template('staff/my_flight.html')

    # if session.get('type') == 'STAFF':
    #     cursor = conn.cursor()
    #     query = "SELECT airline_name FROM airline_staff WHERE username = \'{}\'"
    #     cursor.execute(query.format(session['email']))
    #     data = cursor.fetchone()
    #     cursor.close()
    #     error = None

    #     if(data):
    #         cursor = conn.cursor()
    #         query = "SELECT * FROM flight WHERE airline_name = \'{}\'"
    #         cursor.execute(query.format(data))
    #         data = cursor.fetchone()
    #         cursor.close()
    #         error = None
    #         if(data):
    #             return render_template('staff/my_flight.html', data=data)
    #         else:
    #             error = 'No current flights for this airline exist'
    #             return redirect(url_for('home', error=error))
    #     else:
    #         error = 'Staff does not exist'
    #         return redirect(url_for('login', error=error))

@staff.route('/my-flight', methods=['POST'])
def postMyFlight():
    return render_template('staff/my_flight.html')

@staff.route('/new-flight', methods=['GET','POST'])
def newFlight():
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
            return redirect(url_for('new-flight', error=error))
        else:
            ins = "INSERT INTO flight VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
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
            return redirect(url_for('main.home'))

    return render_template('staff/create_flight.html')

@staff.route('/status', methods=['GET','POST'])
def status():
    return render_template('test.html')

@staff.route('/add-airplane', methods=['GET','POST'])
def addAirplane():
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
            ins = "INSERT INTO airplane VALUES(\'{}\', \'{}\', \'{}\')"
            cursor.execute(ins.format(
               airline_name,
               airplane_id,
               seats))
            conn.commit()
            cursor.close()
            return redirect(url_for('main.home'))

    return render_template('staff/add_airplane.html')

@staff.route('/add-airport', methods=['GET','POST'])
def addAirport():
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
            ins = "INSERT INTO airport VALUES(\'{}\', \'{}\')"
            cursor.execute(ins.format(
               airport_name,
               airport_city))
            conn.commit()
            cursor.close()
            return redirect(url_for('main.home'))

    return render_template('staff/add_airport.html')

@staff.route('/booking-agent', methods=['GET'])
def bookingAgent():
    cursor = conn.cursor()
    query = "SELECT * FROM booking_agent"
    cursor.execute(query.format())
    data = cursor.fetchall()
    cursor.close()
    return render_template('staff/booking_agent.html', agent_list=data)

@staff.route('/customer', methods=['GET','POST'])
def customer():
    cursor = conn.cursor()
    query = "SELECT * FROM customer"
    cursor.execute(query.format())
    data = cursor.fetchall()
    cursor.close()
    return render_template('staff/customer.html', customer_list=data)

@staff.route('/report', methods=['GET','POST'])
def report():
    return render_template('staff/report.html')

@staff.route('/revenue', methods=['GET','POST'])
def revenue():
    labels = ['JAN', 'FEB', 'MAR', 'APR','MAY', 'JUN', 'JUL', 'AUG','SEP', 'OCT', 'NOV', 'DEC']
    values = [967.67, 1190.89, 1079.75, 1349.19,2328.91, 2504.28, 2873.83, 4764.87,4349.29, 6458.30, 9907, 16297]
    return render_template('staff/revenue.html', max=17000, labels=labels, values=values)

@staff.route('/top-destination', methods=['GET','POST'])
def topDestination():
    cursor = conn.cursor()
    query = "SELECT TOP 3 * FROM customer"
    cursor.execute(query.format())
    data = cursor.fetchall()
    cursor.close()
    return render_template('staff/top_destination.html', data=data)
