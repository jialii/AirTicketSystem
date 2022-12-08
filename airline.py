#Import Flask Library
from os import error
from flask import Flask, render_template, request, session, url_for, redirect
#from flask.scaffold import _matching_loader_thinks_module_is_package
import pymysql.cursors
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import hashlib


#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airline',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


# Define a route to hello function
@app.route('/')
def hello():
    # Display flights after the current date only
    todays_date = date.today()
    year = todays_date.year
    month = todays_date.month
    day = todays_date.day
    time_after = '{:02}-{:02}-{:02}'.format(int(year), int(month), int(day))
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE departure_date >= %s'
    cursor.execute(query, (time_after))
    data = cursor.fetchall()
    cursor.close()
    return render_template('homepage.html', posts=data)


# Define route for login
@app.route('/login')
def login():
    return render_template('login.html')


# Define route for register
@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/customerlogin')
def customerlogin():
    return render_template('customerlogin.html')


@app.route('/stafflogin')
def stafflogin():
    return render_template('stafflogin.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        username = session['username']
    except:
        username = None
    try:
        return_date = request.form['return_date']
    except:
        return_date = None
    try:
        round_trip = request.form['round_trip']
    except:
        round_trip = "one-way"
    departure_date = request.form['departure_date']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']

    cursor = conn.cursor()
    if (round_trip == "round-trip"):
        query = "SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s \
                UNION\
                SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s"
        cursor.execute(query, (departure_airport, arrival_airport,
                       departure_date, arrival_airport, departure_airport, return_date))
    else:
        query = "SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s"
        cursor.execute(query, (departure_airport,
                       arrival_airport, departure_date))

    data = cursor.fetchall()
    cursor.close()
    if username:
        return render_template('airline-home.html', posts=data, username=username)
    else:
        return render_template('airline-home.html', posts=data)


@app.route('/searchflights', methods=['GET', 'POST'])
def searchflights():
    try:
        username = session['username']
    except:
        username = None
    try:
        return_date = str(request.form['return_date'])
    except:
        return_date = None
    try:
        round_trip = request.form['round_trip']
    except:
        round_trip = "one-way"
    try:
        departure_date = request.form['departure_date']
        departure_airport = request.form['departure_airport']
        arrival_airport = request.form['arrival_airport']
        cursor = conn.cursor()
        if (round_trip == "round-trip"):
            query = "SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s \
                    UNION\
                    SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s"
            cursor.execute(query, (departure_airport, arrival_airport,
                           departure_date, arrival_airport, departure_airport, return_date))
        else:
            query = "SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s"
            cursor.execute(query, (departure_airport,
                           arrival_airport, departure_date))

        data = cursor.fetchall()
        cursor.close()
        if username:
            return render_template('airline-home.html', posts=data, username=username)
        else:
            return render_template('airline-home.html', posts=data)
    except:
        if username:
            return render_template('airline-home.html', username=username)
        else:
            return render_template('airline-home.html')


@app.route('/flight-city', methods=['GET', 'POST'])
def flight_city():
    try:
        username = session['username']
    except:
        username = None
    try:
        return_date = request.form['return_date']
    except:
        return_date = None
    try:
        round_trip = request.form['round_trip']
    except:
        round_trip = "one-way"
    departure_date = request.form['departure_date']
    departure_city = request.form['departure_city']
    arrival_city = request.form['arrival_city']

    cursor = conn.cursor()
    if (round_trip == "round-trip"):
        query = "SELECT * FROM flight NATURAL JOIN airport WHERE (flight.flight_num) IN \
                (SELECT flight_num FROM flight NATURAL JOIN airport WHERE flight.departure_airport = airport.code AND airport.city = %s AND flight.departure_date = %s) \
                AND flight.arrival_airport = airport.code AND airport.city = %s\
                UNION\
                SELECT * FROM flight NATURAL JOIN airport WHERE (flight.flight_num) IN \
                (SELECT flight_num FROM flight NATURAL JOIN airport WHERE flight.departure_airport = airport.code AND airport.city = %s AND flight.departure_date = %s) \
                AND flight.arrival_airport = airport.code AND airport.city = %s"
        cursor.execute(query, (departure_city, departure_date,
                       arrival_city, arrival_city, return_date, departure_city))
    else:
        query = "SELECT * FROM flight NATURAL JOIN airport WHERE (flight.flight_num) IN \
            (SELECT flight_num FROM flight NATURAL JOIN airport WHERE flight.departure_airport = airport.code AND airport.city = %s AND flight.departure_date = %s) \
                AND flight.arrival_airport = airport.code AND airport.city = %s;"
        cursor.execute(query, (departure_city, departure_date, arrival_city))

    data = cursor.fetchall()
    cursor.close()
    if username:
        return render_template('airline-home.html', posts=data, username=username)
    else:
        return render_template('airline-home.html', posts=data)


@app.route('/status', methods=['GET', 'POST'])
def status():
    try:
        username = session['username']
    except:
        username = None
    cursor = conn.cursor()
    if request.form['flight num'] == '':
        query = "SELECT flight_num, status FROM flight"
        cursor.execute(query)
    else:
        flight_num = int(request.form['flight num'])
        query = "SELECT flight_num, status FROM flight WHERE flight_num = %s"
        cursor.execute(query, [flight_num])

    data = cursor.fetchall()
    cursor.close()
    return render_template('airline-home.html', status=data, username=username)


# Authenticates the login
@app.route('/customerloginAuth', methods=['GET', 'POST'])
def customerloginAuth():
    # grabs information from the forms
    username = request.form['username']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM customer WHERE email = %s and password = %s'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        # creates a session for the the user
        # session is a built in
        session['username'] = username
        return redirect(url_for('customerhome'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('customerlogin.html', error=error)


# Authenticates the login
@app.route('/staffloginAuth', methods=['GET', 'POST'])
def staffloginAuth():
    # grabs information from the forms
    username = request.form['username']
    password = hashlib.md5((request.form['password']).encode()).hexdigest()
    print(password)

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM airlinestaff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        # creates a session for the the user
        # session is a built in
        session['username'] = username
        return redirect(url_for('staffhome'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('stafflogin.html', error=error)


@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    identity = request.form['identity']
    if identity == None:
        error = 'You must choose your account type'
        return render_template(error=error)
    if not (identity == 'staff' and identity == 'customer'):
        if identity == 'staff':
            return render_template('staffRegister.html')
        elif identity == 'customer':
            return render_template('customerRegister.html')
        else:
            error = 'You can only choose one account type'
            return render_template('register.html', error=error)


@app.route('/staffRegister', methods=['GET', 'POST'])
def staffRegister():
    error = None
    cursor = conn.cursor()
    username = request.form['username']
    password = hashlib.md5((request.form['password']).encode()).hexdigest()
    passwordtwo = hashlib.md5(
        (request.form['passwordtwo']).encode()).hexdigest()
    print(password, 'password')
    print(passwordtwo, 'passwordtwo')

    if (password != passwordtwo):
        error = 'The second entry of your password does not match the previous one'
        return render_template('staffRegister.html', error=error)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    airline_name = request.form['airline_name']
    phone_number = request.form.getlist('phone_number[]')

    query = 'SELECT * FROM airlinestaff WHERE username = %s'
    cursor.execute(query, username)
    data = cursor.fetchall()
    if(data):
        error = "This username already exists."
        cursor.close()
        return render_template('staffRegister.html', error=error)
    else:
        ins = 'INSERT INTO airlinestaff(username, password,first_name,last_name,date_of_birth,\
                airline_name) VALUES(%s,%s,%s,%s,%s,%s)'
        query = 'SELECT * FROM Airline WHERE airline_name = %s'
        cursor.execute(query, airline_name)
        data = cursor.fetchall()
        if (data):
            pass
        else:
            query = 'INSERT INTO Airline(airline_name) VALUES(%s)'
            cursor.execute(query, airline_name)

        cursor.execute(ins, (username, password, first_name,
                       last_name, dob, airline_name))
        conn.commit()

    query = 'SELECT * FROM airlinestaff WHERE username = %s'
    cursor.execute(query, username)
    data = cursor.fetchall()
    if(data):
        for item in phone_number:
            cursor.execute(
                ("INSERT INTO Phone(username,phone_number) VALUES(%s,%s)"), (username, item))
        conn.commit()
        cursor.close()
        session['username'] = username
        return redirect(url_for('staffhome'))
    else:
        error = "Something went wrong. Please try again."
        return render_template('staffRegister.html', register_error=error)


@app.route('/customerRegister', methods=['GET', 'POST'])
def customerRegister():
    cursor = conn.cursor()
    error = None

    password = hashlib.md5((request.form['password']).encode()).hexdigest()
    passwordtwo = hashlib.md5(
        (request.form['passwordtwo']).encode()).hexdigest()
    if not (password == passwordtwo):
        error = 'The second entry of your password does not match the previous one'

        return render_template('customerRegister.html', error=error)

    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    phone_number = request.form['phone_number']

    street = request.form['street']
    building_num = request.form['building_num']
    city = request.form['city']
    state = request.form['state']
    pass_num = request.form['passport_number']
    pass_cou = request.form['passport_country']
    pass_ex = request.form['passport_exp_date']

    query1 = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query1, email)
    data1 = cursor.fetchall()

    query2 = 'SELECT * FROM customer WHERE passport_number = %s'
    cursor.execute(query2, pass_num)
    data2 = cursor.fetchall()

    if(data1):
        error = "This email has already been used"
        cursor.close()
        return render_template('customerRegister.html', register_error=error)
    elif(data2):
        error = "This passport has already been used"
        cursor.close()
        return render_template('customerRegister.html', register_error=error)
    else:
        ins = 'INSERT INTO customer(password,email,first_name,last_name,date_of_birth,\
                street,building_number,city,state,passport_number,passport_expiration,\
                passport_country) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(ins, (password, email, first_name, last_name, dob,
                             street, building_num, city, state, pass_num, pass_ex, pass_cou))

        session['username'] = email

        conn.commit()
        cursor.close()
        return redirect(url_for('customerhome'))


@app.route('/customerhome')
def customerhome():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT first_name, last_name from customer WHERE email=%s'
    cursor.execute(query, username)
    name = cursor.fetchall()[0]
    return render_template('customerhome.html', username=username, name=name)


@app.route('/staffhome')
def staffhome():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT first_name, last_name from airlinestaff WHERE username=%s'
    cursor.execute(query, username)
    name = cursor.fetchall()[0]
    return render_template('staffhome.html', name=name)


@app.route('/viewmyflights', methods=['GET', 'POST'])
def viewmyflights():
    username = session['username']
    startdate = None
    enddate = None
    airport = None
    cursor = conn.cursor()

    query = 'SELECT departure_airport From flight NATURAL JOIN ticket WHERE email = %s'
    cursor.execute(query, (username))
    d_airports = cursor.fetchall()

    query = 'SELECT arrival_airport From flight NATURAL JOIN ticket WHERE email = %s'
    cursor.execute(query, (username))
    a_airports = cursor.fetchall()

    try:
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        query = 'SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM ticket WHERE email = %s) AND departure_date BETWEEN %s AND %s ORDER BY departure_date'
        cursor.execute(query, (username, startdate, enddate))
        data = cursor.fetchall()
        typeofdisplay = 'range_of_dates'
    except:
        try:
            source_airport = request.form['departure_airport']
            query = 'SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM ticket WHERE email = %s) AND departure_airport =%s'
            cursor.execute(query, (username, source_airport))
            data = cursor.fetchall()
            typeofdisplay = 'source_airport'
            airport = source_airport
        except:
            try:
                destination_airport = request.form['arrival_airport']
                query = 'SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM ticket WHERE email = %s) AND arrival_airport =%s'
                cursor.execute(query, (username, destination_airport))
                data = cursor.fetchall()
                typeofdisplay = 'destination_airport'
                airport = destination_airport
            except:
                if request.form.get('allflights'):
                    query = 'SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM ticket WHERE email = %s)'
                    cursor.execute(query, (username))
                    data = cursor.fetchall()
                    typeofdisplay = 'allmyflights'
                else:
                    query = 'SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM ticket WHERE email = %s) AND departure_date BETWEEN CURRENT_TIMESTAMP AND DATE_ADD(DATE(CURRENT_TIMESTAMP), INTERVAL 30 DAY)'
                    cursor.execute(query, (username))
                    data = cursor.fetchall()
                    typeofdisplay = 'deafult_flightsfor_next30days'
    cursor.close()
    return render_template('viewmyflights.html', username=username, flights=data, typeofdisplay=typeofdisplay, airport=airport, startdate=startdate, enddate=enddate, d_airports=d_airports, a_airports=a_airports)


@app.route('/viewrevenue')
def viewrevenue():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    airline_name = data['airline_name']

    # Get one year time range
    todays_date = date.today()
    delta = datetime.timedelta(days=365)
    one_year_ago = todays_date - delta
    time_after = '{:02}-{:02}-{:02} {:02}:{:02}:{:02}'.format(
        int(one_year_ago.year), int(one_year_ago.month), int(one_year_ago.day), 0, 0, 0)
    query = 'SELECT * FROM ticket AS t WHERE airline_name = %s AND purchase_date_time > %s'
    cursor.execute(query, (airline_name, time_after))
    data = cursor.fetchall()
    total_revenue = sum([item['sold_price'] for item in data])

    # Get one month time range
    delta = datetime.timedelta(days=30)
    one_month_ago = todays_date - delta
    time_after = '{:02}-{:02}-{:02} {:02}:{:02}:{:02}'.format(int(
        one_month_ago.year), int(one_month_ago.month), int(one_month_ago.day), 0, 0, 0)
    query = 'SELECT * FROM ticket AS t WHERE airline_name = %s AND purchase_date_time > %s'
    cursor.execute(query, (airline_name, time_after))
    data = cursor.fetchall()
    month_revenue = sum([item['sold_price'] for item in data])

    return render_template('revenue.html', username=username, year_total=total_revenue, month_total=month_revenue)


@app.route('/viewflights', methods=['GET', 'POST'])
def viewflights():
    username = session['username']
    airport = None
    startdate = None
    enddate = None
    cursor = conn.cursor()

    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (username))
    tempdata = cursor.fetchone()
    airline_name = tempdata['airline_name']

    query = 'SELECT departure_airport From flight WHERE airline_name = %s'
    cursor.execute(query, (airline_name))
    d_airports = cursor.fetchall()

    query = 'SELECT arrival_airport From flight WHERE airline_name = %s'
    cursor.execute(query, (airline_name))
    a_airports = cursor.fetchall()

    try:
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        query = 'SELECT * FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s ORDER BY departure_date'
        cursor.execute(query, (airline_name, startdate, enddate))
        data = cursor.fetchall()
        typeofdisplay = 'range_of_dates'
    except:
        try:
            source_airport = request.form['departure_airport']
            query = 'SELECT * FROM flight WHERE airline_name = %s AND departure_airport =%s'
            cursor.execute(query, (airline_name, source_airport))
            data = cursor.fetchall()
            typeofdisplay = 'source_airport'
            airport = source_airport
        except:
            try:
                destination_airport = request.form['arrival_airport']
                query = 'SELECT * FROM flight WHERE airline_name = %s AND arrival_airport =%s'
                cursor.execute(query, (airline_name, destination_airport))
                data = cursor.fetchall()
                typeofdisplay = 'destination_airport'
                airport = destination_airport
            except:
                query = 'SELECT * FROM flight WHERE airline_name = %s AND departure_date BETWEEN CURRENT_TIMESTAMP AND DATE_ADD(DATE(CURRENT_TIMESTAMP), INTERVAL 30 DAY)'
                cursor.execute(query, (airline_name))
                data = cursor.fetchall()
                typeofdisplay = 'deafult_flightsfor_next30days'
    cursor.close()
    return render_template('viewflights.html', username=username, flights=data, airline_name=airline_name, typeofdisplay=typeofdisplay, d_airports=d_airports, a_airports=a_airports, airport=airport, startdate=startdate, enddate=enddate)


@app.route('/viewcustomers')
def viewcustomers():
    cursor = conn.cursor()
    username = session['username']
    flight_num = request.args.get('flight_num')
    query = 'SELECT * FROM customer WHERE email IN (SELECT email FROM ticket WHERE flight_num = %s)'
    cursor.execute(query, (flight_num))
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewcustomers.html', customers=data, flight_num=flight_num)


@app.route('/purchasetickets')
def purchasetickets():
    try:
        username = session['username']
    except:
        username = None
    # Display flights after the current date only
    todays_date = date.today()
    year = todays_date.year
    month = todays_date.month
    day = todays_date.day
    time_after = '{:02}-{:02}-{:02}'.format(int(year), int(month), int(day))
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE departure_date >= %s'
    cursor.execute(query, (time_after))
    data = cursor.fetchall()
    cursor.close()

    return render_template('purchasetickets.html', username=username, posts=data)


@app.route('/purchaseAuth', methods=['GET', 'POST'])
def purchaseAuth():
    try:
        username = session['username']
    except:
        username = None
    try:
        flight_number = int(request.form['flight_num'])
        card_type = request.form['card_type']
        card_number = request.form['card_number']
        name_on_card = request.form['name_on_card']
        expiration_date = request.form['expiration_date'] + '-01'

        cursor = conn.cursor()

        now = datetime.datetime.now()
        current_time = '{:02}-{:02}-{:02} {:02}:{:02}:{:02}'.format(
            int(now.year), int(now.month), int(now.day), int(now.hour), int(now.minute), int(now.second))

        query = 'SELECT departure_date FROM flight WHERE flight_num = %s'
        cursor.execute(query, (flight_number))
        departure_date = cursor.fetchone(
        )['departure_date'].strftime("%Y-%m-%d")

        query = 'SELECT departure_time FROM flight WHERE flight_num = %s'
        cursor.execute(query, (flight_number))
        s = cursor.fetchone()['departure_time'].seconds
        hours = s // 3600
        s = s - (hours * 3600)
        minutes = s // 60
        seconds = s - (minutes * 60)
        departure_time = '{:02}:{:02}:{:02}'.format(
            int(hours), int(minutes), int(seconds))

        departure_date_time = departure_date + ' ' + departure_time

        if not departure_date_time > current_time:
            error = "Cannot purchase a past flight."
            return render_template('purchasetickets.html', username=username, error=error)

        query = 'SELECT airline_name FROM flight WHERE flight_num = %s'
        cursor.execute(query, (flight_number))
        airline_name = cursor.fetchone()['airline_name']

        query = 'SELECT base_price FROM flight WHERE flight_num = %s'
        cursor.execute(query, (flight_number))
        base_price = float(cursor.fetchone()['base_price'])

        query = 'SELECT COUNT(distinct ticket_id) as booked_counts FROM ticket WHERE flight_num = %s'
        cursor.execute(query, (flight_number))
        booked_seats = cursor.fetchall()[0]['booked_counts']

        query = 'SELECT id_num FROM flight WHERE flight_num = %s'
        cursor.execute(query, (int(flight_number)))
        id_num = int(cursor.fetchone()['id_num'])

        query = 'SELECT num_seats FROM airplane WHERE id_num = %s'
        cursor.execute(query, (int(id_num)))
        total_seats = int(cursor.fetchone()['num_seats'])

        query = 'SELECT * FROM ticket'
        cursor.execute(query)
        data = cursor.fetchall()

        for tkt in data:
            if (tkt['email'] == username and int(tkt['flight_num']) == flight_number):
                error = "Already booked this flight."
                return render_template('purchasetickets.html', username=username, error=error)

        if data == ():
            # create a ticket
            purchase_id = 1
            # calculate ticket price: If 75% of the capacities is already booked, add 25% to the base price.
            sold_price = base_price
            # create a ticket
            query = 'INSERT INTO ticket (email, ticket_id, sold_price, card_type, card_number, \
                        name_on_card, expiration_date, purchase_date_time, flight_num, \
                        departure_date, departure_time, airline_name) VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP(), %s, %s, %s, %s)'
            cursor.execute(query, (username, purchase_id, sold_price, card_type, card_number, name_on_card, expiration_date,
                                   flight_number, departure_date, departure_time, airline_name))
        else:
            # create a ticket
            id_list = [int(line['ticket_id']) for line in data]
            purchase_id = max(id_list)+1
            # calculate ticket price: If 75% of the capacities is already booked, add 25% to the base price.
            if booked_seats >= total_seats:
                error = "No seats on flight."
                return render_template('purchasetickets.html', username=username, error=error)
            elif (booked_seats+1) >= 0.75*total_seats:
                sold_price = base_price*1.25
                sold_price = round(sold_price, 2)
            else:
                sold_price = base_price
            # create a ticket
            query = 'INSERT INTO ticket (email, ticket_id, sold_price, card_type, card_number, \
                        name_on_card, expiration_date, purchase_date_time, flight_num, \
                        departure_date, departure_time, airline_name) VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP(), %s, %s, %s, %s)'
            cursor.execute(query, (username, purchase_id, sold_price, card_type, card_number, name_on_card, expiration_date,
                                   flight_number, departure_date, departure_time, airline_name))
        conn.commit()
        cursor.close()
    except:
        error = "Purchase was unsuccessful."
        return render_template('purchasetickets.html', username=username, error=error)

    # Display flights after the current date only
    todays_date = date.today()
    year = todays_date.year
    month = todays_date.month
    day = todays_date.day
    time_after = '{:02}-{:02}-{:02}'.format(int(year), int(month), int(day))
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE departure_date >= %s'
    cursor.execute(query, (time_after))
    data = cursor.fetchall()
    cursor.close()

    message = "Purchase confirmed."
    return render_template('purchasetickets.html', username=username, posts=data, message=message)


@app.route('/ratings')
def ratings():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT * FROM rates WHERE email = %s'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    query = 'SELECT flight_num FROM ticket WHERE email = %s AND flight_num IN (SELECT flight_num FROM flight WHERE arrival_date < CURRENT_TIMESTAMP)'
    cursor.execute(query, (username))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('ratings.html', ratings=data1, flights=data2)


@app.route('/addrating', methods=['GET', 'POST'])
def addrating():
    email = session['username']
    cursor = conn.cursor()
    flight_num = request.form['flight_num']
    ratings = request.form['ratings']
    comments = request.form['comments']
    query = 'INSERT INTO rates (email, flight_num, ratings, comments) VALUES(%s, %s, %s, %s)'
    cursor.execute(query, (email, flight_num, ratings, comments))
    conn.commit()
    cursor.close()
    return redirect(url_for('ratings'))


@app.route('/trackspending', methods=['GET', 'POST'])
def trackspending():
    username = session['username']
    # Get past year spending
    todays_date = date.today()
    year = todays_date.year
    year = year-1
    month = todays_date.month
    day = todays_date.day
    time_after = '{:02}-{:02}-{:02} {:02}:{:02}:{:02}'.format(
        int(year), int(month), int(day), 0, 0, 0)
    cursor = conn.cursor()
    query = 'SELECT * FROM ticket AS t WHERE email = %s AND purchase_date_time > %s'
    cursor.execute(query, (username, time_after))
    data = cursor.fetchall()
    total_spendings = sum([item['sold_price'] for item in data])

    try:
        start_month = request.form['start_month']
        end_month = request.form['end_month']
        start_ls = start_month.split('-')
        end_ls = end_month.split('-')
        start_yr = int(start_ls[0])
        start_month = int(start_ls[1])
        end_yr = int(end_ls[0])
        end_month = int(end_ls[1])
        result = []
        start = datetime.date(start_yr, start_month, 1)
        end = datetime.date(end_yr, end_month, 1)
        while start <= end:
            result.append(start)
            start += relativedelta(months=1)
        select_range = True
    except:
        # Get monthly - default
        current = datetime.date.today() + relativedelta(months=-6)
        result = []
        today = datetime.date.today()
        while current <= today:
            result.append(current)
            current += relativedelta(months=1)
        result = result[-6:]
        select_range = False

    get_months = [(int(dateitem.year), int(dateitem.month))
                  for dateitem in result]
    bar_labels = [labels[item[1]-1] for item in get_months]

    total_values = 0
    bar_values = []
    for mon in get_months:
        time_after = '{:02}-{:02}-{:02} {:02}:{:02}:{:02}'.format(
            int(mon[0]), int(mon[1]), 1, 0, 0, 0)
        if mon[1] != 12:
            time_before = '{:02}-{:02}-{:02} {:02}:{:02}:{:02}'.format(
                int(mon[0]), int(mon[1])+1, 1, 0, 0, 0)
        else:
            time_before = '{:02}-{:02}-{:02} {:02}:{:02}:{:02}'.format(
                int(mon[0])+1, 1, 1, 0, 0, 0)
        query = 'SELECT * FROM ticket AS t WHERE email = %s AND purchase_date_time >= %s AND purchase_date_time < %s'
        cursor.execute(query, (username, time_after, time_before))
        data = cursor.fetchall()
        monthly_spendings = sum([item['sold_price'] for item in data])
        bar_values.append(monthly_spendings)
        total_values += monthly_spendings

    cursor.close()
    if not select_range:
        return render_template('trackspending.html', year_total=total_spendings, title='Spending in the past 6 months in USD', max=max(bar_values), labels=bar_labels, values=bar_values, username=username)
    else:
        return render_template('trackspending.html', monthly_total=total_values, title='Spending in the selected months in USD', max=max(bar_values), labels=bar_labels, values=bar_values, username=username)


@app.route('/createflights', methods=['GET', 'POST'])
def createflights():
    username = session['username']
    cursor = conn.cursor()

    query = 'SELECT * FROM flight WHERE airline_name IN (SELECT airline_name FROM flight \
            NATURAL JOIN airlinestaff WHERE username = %s) AND departure_date BETWEEN CURRENT_TIMESTAMP AND DATE_ADD(DATE(CURRENT_TIMESTAMP), INTERVAL 30 DAY)'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()

    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']

    query = 'SELECT id_num FROM airplane WHERE airline_name = %s'
    cursor.execute(query, (airline_name))
    airplanes = cursor.fetchall()

    query = 'SELECT code FROM airport'
    cursor.execute(query)
    airports = cursor.fetchall()

    try:
        flight_num = request.form['flight_num']
        departure_date = (request.form['departure_date'])
        departure_date = str(departure_date)
        departure_time = request.form['departure_time']
        departure_airport = request.form['departure_airport']
        arrival_date = request.form['arrival_date']
        arrival_time = request.form['arrival_time']
        arrival_airport = request.form['arrival_airport']
        base_price = request.form['base_price']
        status = request.form['status']
        airplane_id = request.form['airplane_id']
        query = 'INSERT INTO flight(flight_num, departure_date, departure_time, departure_airport, \
                arrival_date, arrival_time, arrival_airport, base_price, status, airline_name, id_num) \
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (flight_num, departure_date, departure_time, departure_airport, arrival_date,
                               arrival_time, arrival_airport, base_price, status, airline_name, airplane_id))
        conn.commit()
        query = 'SELECT * FROM flight WHERE airline_name IN (SELECT airline_name FROM flight \
                NATURAL JOIN airlinestaff WHERE username = %s) AND departure_date BETWEEN CURRENT_TIMESTAMP AND DATE_ADD(DATE(CURRENT_TIMESTAMP), INTERVAL 30 DAY)'
        cursor.execute(query , (username))
        data1 = cursor.fetchall()
    except:
        pass
    cursor.close()
    return render_template('createflights.html', flights=data1, airline_name=airline_name, airplanes=airplanes, airports=airports)


@app.route('/changestatus', methods=['GET', 'POST'])
def changestatus():
    username = session['username']
    cursor = conn.cursor()
    todays_date = date.today()
    query = 'SELECT flight_num, id_num, departure_date, departure_time, departure_airport, \
            arrival_date, arrival_time, arrival_airport, base_price, status, airline_name \
            FROM airlinestaff NATURAL JOIN flight WHERE username = %s and departure_date > %s'
    cursor.execute(query, (username, todays_date))
    data = cursor.fetchall()

    try:
        status = request.form.get('status')
        flight = request.form.getlist('mycheckbox')
        for num in flight:
            query1 = 'UPDATE Flight SET status = %s WHERE flight_num = %s'
            cursor.execute(query1, (status, num))

        conn.commit()

        query = 'SELECT flight_num, id_num, departure_date, departure_time, departure_airport, \
            arrival_date, arrival_time, arrival_airport, base_price, status, airline_name \
            FROM airlinestaff NATURAL JOIN flight WHERE username = %s and departure_date > %s'
        cursor.execute(query, (username, todays_date))
        data = cursor.fetchall()

    except:
        error = "Something went wrong, please try again."
        return render_template('changestatus.html', error=error)

    cursor.close()
    return render_template('changestatus.html', flights=data)


@app.route('/addairplane', methods=['GET', 'POST'])
def addairplane():
    error = None
    cursor = conn.cursor()
    username = session['username']
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    myairline = data['airline_name']

    query = "SELECT * FROM Airplane WHERE airline_name = %s"
    cursor.execute(query, myairline)
    airplane = cursor.fetchall()

    try:
        airplane_id = request.form['airplane_id']
        num_seats = request.form['num_seats']

        ins = 'INSERT INTO Airplane(id_num,num_seats,airline_name) VALUES(%s,%s,%s)'
        cursor.execute(ins, (airplane_id, num_seats, myairline))

        conn.commit()
        query = "SELECT * FROM Airplane WHERE airline_name = %s"
        cursor.execute(query, myairline)
        airplane = cursor.fetchall()

    except:
        error = "Something went wrong, please try again"
        return render_template('addairplane.html', username=username, airplane=airplane, error=error)

    cursor.close()
    message = "You have added a new airplane successfully."
    return render_template('addairplane.html', username=username, airplane=airplane, message=message)


@app.route('/addairport', methods=['GET', 'POST'])
def addairport():
    cursor = conn.cursor()
    username = session['username']
    query = 'Select * FROM airport'
    cursor.execute(query)
    data = cursor.fetchall()
    try:
        code = request.form['code']
        airport_name = request.form['airport_name']
        city = request.form['city']
        query = 'INSERT INTO airport(code, airport_name, city) VALUES(%s,%s,%s)'
        cursor.execute(query, (code, airport_name, city))
        conn.commit()
        cursor = conn.cursor()
        username = session['username']
        query = 'Select * FROM airport'
        cursor.execute(query)
        data = cursor.fetchall()
    except:
        pass
    cursor.close()
    return render_template('addairport.html', airports=data)


@app.route('/viewratings')
def viewratings():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT * FROM rates WHERE flight_num IN (SELECT flight_num FROM flight WHERE airline_name IN (SELECT airline_name FROM airlinestaff WHERE username = %s)) ORDER BY flight_num'
    cursor.execute(query, username)
    data = cursor.fetchall()
    averages = {}
    for line in data:
        if line['flight_num'] in averages:
            averages[line['flight_num']].append(line['ratings'])
        else:
            averages[line['flight_num']] = [line['ratings']]
    for key in averages:
        temp_sum = 0
        temp_count = 0
        for value in averages[key]:
            temp_sum += value
            temp_count += 1
        theaverage = temp_sum / temp_count
        averages[key] = theaverage
    cursor.close()
    return render_template('viewratings.html', username=username, ratings=data, averages=averages)


@app.route('/viewfrequent', methods=['GET', 'POST'])
def viewfrequent():
    cursor = conn.cursor()
    username = session['username']
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    airline_name = data['airline_name']

    query = "SELECT DISTINCT email, COUNT(email) AS num, first_name, last_name, date_of_birth FROM Ticket NATURAL JOIN Customer WHERE Customer.first_name = Ticket.name_on_card and Ticket.airline_name = %s  GROUP BY email"
    cursor.execute(query, (airline_name))
    customerdata = cursor.fetchall()
    customerdata = sorted(customerdata, key=lambda i: i['num'], reverse=True)
    ticket_num = sum(purchase['num']for purchase in customerdata)
    return render_template('viewfrequent.html', username=username, info=customerdata, ticket_num=ticket_num)


@app.route('/customerflights', methods=['GET', 'POST'])
def customerflights():
    cursor = conn.cursor()
    username = session['username']
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    airline_name = data['airline_name']

    #customer = 'alice@gmail.com'
    customer = request.form['cust_email']

    query = 'SELECT * FROM ticket NATURAL JOIN Customer WHERE email = %s AND airline_name=%s'
    cursor.execute(query, (customer, airline_name))
    data = cursor.fetchall()
    cursor.close()
    return render_template('customerflights.html', username=username, tickets=data)


@app.route('/viewtopdestinations', methods=['GET', 'POST'])
def viewtopdestinations():
    cursor = conn.cursor()
    username = session['username']
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    airline_name = data['airline_name']
    todays_date = date.today()
    year = todays_date.year
    month = todays_date.month
    day = todays_date.day

    try:
        period = request.form.get('timerange')
        if period == "year":
            year = year-1
        else:
            month = month - 3

    except:
        pass

    range = '{:02}-{:02}-{:02} {:02}:{:02}:{:02}'.format(
        int(year), int(month), int(day), 0, 0, 0)

    query = "SELECT arrival_airport, COUNT(Flight.arrival_airport) AS num FROM Flight NATURAL JOIN \
            Ticket WHERE Flight.flight_num=Ticket.flight_num AND purchase_date_time > %s \
                AND airline_name = %s GROUP BY arrival_airport LIMIT 3"
    cursor.execute(query, (range, airline_name))
    data = cursor.fetchall()

    data = sorted(data, key=lambda i: i['num'], reverse=True)

    ticket_num = sum(purchase['num']for purchase in data)
    return render_template('viewtopdestinations.html', info=data, ticket_num=ticket_num)


@app.route('/viewreports', methods=['GET', 'POST'])
def viewreports():
    username = session['username']
    cursor = conn.cursor()
    try:
        if request.form.get('displayflights') == 'lastmonth':
            main_display = 'lastmonth'
            query = 'SELECT MONTH(purchase_date_time) as month, YEAR(purchase_date_time) as year, COUNT(ticket_id) AS total FROM ticket WHERE airline_name IN (SELECT airline_name FROM airlinestaff WHERE username = %s) AND MONTH(purchase_date_time) = (MONTH(CURRENT_TIMESTAMP)-1) GROUP BY MONTH(purchase_date_time)'
        elif request.form.get('displayflights') == 'lastyear':
            main_display = 'lastyear'
            query = 'SELECT MONTH(purchase_date_time) as month, YEAR(purchase_date_time) as year, COUNT(ticket_id) AS total FROM ticket WHERE airline_name IN (SELECT airline_name FROM airlinestaff WHERE username = %s) AND YEAR(purchase_date_time) = (YEAR(CURRENT_TIMESTAMP)-1) GROUP BY MONTH(purchase_date_time) ORDER BY purchase_date_time'
        cursor.execute(query, (username))
        data1 = cursor.fetchall()
    except:
        main_display = 'allflights'
        query = 'SELECT MONTH(purchase_date_time) as month, YEAR(purchase_date_time) as year, COUNT(ticket_id) AS total FROM ticket WHERE airline_name IN (SELECT airline_name FROM airlinestaff WHERE username = %s) GROUP BY MONTH(purchase_date_time) ORDER BY purchase_date_time'
        cursor.execute(query, (username))
        data1 = cursor.fetchall()
    try:
        start = request.form['startdate']
        end = request.form['enddate']
        query = 'SELECT MONTH(purchase_date_time) as month, YEAR(purchase_date_time) as year, COUNT(ticket_id) AS total FROM ticket WHERE airline_name IN (SELECT airline_name FROM airlinestaff WHERE username = %s) AND purchase_date_time > %s AND purchase_date_time < %s GROUP BY MONTH(purchase_date_time) ORDER BY purchase_date_time'
        cursor.execute(query, (username, start, end))
        data2 = cursor.fetchall()
        for line in data1:
            line['month'] = months[(line['month'] - 1)]
        for line in data2:
            line['month'] = months[(line['month'] - 1)]
        cursor.close()
        return render_template('viewreports.html', username=username, tickets=data1, specify=data2, main_display=main_display)
    except:
        for line in data1:
            line['month'] = months[(line['month'] - 1)]
        cursor.close()
        return render_template('viewreports.html', username=username, tickets=data1, specify=None, main_display=main_display)


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
