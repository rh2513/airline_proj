# import packages from Flask Lib
from flask import Flask, render_template, request, session, url_for, redirect, flash
from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Page
import random


import pymysql.cursors

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

conn = pymysql.connect(host='localhost',
                user='root',
                port=3306,
                password='',
                db='airport_proj',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'some key that you will never guess'

from main import main_routes
app.register_blueprint(main_routes.main)

from auth import auth_routes
app.register_blueprint(auth_routes.auth)

from staff import staff_routes
app.register_blueprint(staff_routes.staff)

@app.route('/customer_home')
def customer_home():
	try:
		usertype = session['type']
		if usertype == "Customer":
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
		if usertype == "Customer":
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
		if usertype == "Customer":
			return render_template('c_search.html')
		else:
			return render_template('error.html')
	except KeyError:
		return render_template('error.html')


@app.route('/c_searchAuth', methods = ['GET','POST'])
def c_searchAuth():
	try:
		usertype = session['type']
		if usertype == "Customer":
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
		if usertype == "Customer":
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
		if usertype == "Customer":
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


@app.route('/c_spending')
def c_spending():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Customer":
			cursor = conn.cursor()
			query = 'SELECT sum(price) as sum FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE())'
			cursor.execute(query, (username))
			data = cursor.fetchall()
			cursor.close()
			error = None
			print(data)
			if (data):
				cursor = conn.cursor()
				query = 'SELECT month(purchase_date) as month, sum(price) as money1 FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 6 MONTH) AND CURRENT_DATE()) GROUP BY month ORDER BY month'
				cursor.execute(query, (username))
				bardata = cursor.fetchall()
				cursor.close()
				print(bardata)
				bar = Bar('Track my Spending within 6 months')
				xbar = []
				ybar =[]
				for dic in bardata:
					xbar.append(dic['month'])
					ybar.append(int(dic['money1']))
				print(xbar,ybar)
				bar.add('money',xbar,ybar)
				return render_template('c_tracker.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
			else:
				error = "You have not get any ticket."
				return render_template('c_tracker.html', error = error)
		else:
			return render_template('error.html')
	except KeyError:
		return render_template('error.html')

@app.route('/c_details')
def c_details():
	return render_template('c_details.html')

@app.route('/c_detailsAuth', methods = ['GET', 'POST'])
def c_detailsAuth():
	try:
		username = session['value']
		usertype = session['type']
		if usertype == "Customer":
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
				query = 'SELECT month(purchase_date) as month, sum(price) as money1 FROM flight natural join ticket natural join purchases WHERE customer_email = %s AND (purchase_date BETWEEN %s AND %s) GROUP BY month ORDER BY month'
				cursor.execute(query, (username, date_start, date_end))
				bardata = cursor.fetchall()
				cursor.close()
				bar = Bar('Track my Spending in a range')
				xbar = []
				ybar =[]
				for dic in bardata:
					xbar.append(dic['month'])
					ybar.append(int(dic['money1']))
				bar.add('money',xbar,ybar)
				return render_template('c_details.html', post = data, myechart = bar.render_embed(), host = REMOTE_HOST, script_list=bar.get_js_dependencies())
			else:
				error = "You have not get any ticket."
				return render_template('c_details.html', error = error)
		else:
			return render_template('error.html')
	except KeyError:
		return render_template('error.html')


                
if __name__ == '__main__':
    app.run(debug=True)
