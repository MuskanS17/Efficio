from flask import Flask, request, redirect, session
from flask import render_template, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

from algorithms.rr import rr
from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.hrrn import hrrn
from algorithms.fifo import fifo
from algorithms.lru import lru
from algorithms.optimal import optimal

app=Flask(__name__)
app.secret_key = "secret"


# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "DummyPassword"  # Change if needed
app.config["MYSQL_DB"] = "user_db"
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/scheduler")
def login():
    return render_template("schedular.html")

@app.route("/scheduler1")
def schedular():
    return render_template("schedular.html")

@app.route("/page_fault")
def page_fault():
    return render_template("page.html")
@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):  # user[2] is the password field
            session['user_id'] = user[0]  # Store user id in session
            session['username'] = user[1]  # Store username in session
            # flash('Login successful!', 'success')
            #return redirect(url_for('scheduler'))
            return render_template('schedular.html')
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login_page'))

    return render_template('login1.html')


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login_page'))

    return render_template('register1.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))
    # return render_template("index.html")


@app.route('/algo', methods=['GET', 'POST'])
def algo():
    if request.method == 'POST':
        num_processes = int(request.form.get('num_processes'))
        # print(num_processes,flush=True)
        if ',' in request.form.get('arrival_times'):
            arrival_times = list(map(int, request.form.get('arrival_times').split(',')))
        else:
            arrival_times=[0]
        if ',' in request.form.get('burst_times'):
            burst_times = list(map(int, request.form.get('burst_times').split(',')))
        else:
            burst_times=[0]
        algorithm = request.form.get('algorithm')
        
        if algorithm == 'fcfs':
            at, bt, completion_times, waiting_times, turnaround_times, avg_wt, avg_tat = fcfs(arrival_times, burst_times)
        elif algorithm == 'sjf':
            at,bt, completion_times, waiting_times, turnaround_times, avg_wt, avg_tat = sjf(arrival_times, burst_times)
        elif algorithm == 'srtf':
            at,bt, completion_times, waiting_times, turnaround_times, avg_wt, avg_tat = srtf(arrival_times, burst_times)
        elif algorithm == 'hrrn':
            at,bt, completion_times, waiting_times, turnaround_times, avg_wt, avg_tat = hrrn(arrival_times, burst_times)
        elif algorithm == 'rr':
            if request.form.get('quantum').isdigit():
                quantum= int(request.form.get('quantum'))
            else:
                quantum=1
            at,bt,ct,wt,tat, avg_wt, avg_tat = rr(arrival_times, burst_times, quantum)
            results="results"
            return render_template('scheduling.html',results=results, num_processes=num_processes, at=at, bt=bt, 
                               completion_times=ct, waiting_times=wt, turnaround_times=tat, 
                               avg_wt=avg_wt, avg_tat=avg_tat)
        results="results"
        return render_template('scheduling.html',results=results, num_processes=num_processes, at=at, bt=bt, 
                               completion_times=completion_times, waiting_times=waiting_times, turnaround_times=turnaround_times, 
                               avg_wt=avg_wt, avg_tat=avg_tat)
    
    return render_template('scheduling.html')


@app.route('/page', methods=['GET', 'POST'])
def page():
    if request.method == 'POST':
        if ',' in request.form['page_reference']:
            page_reference = list(map(int, request.form['page_reference'].split(',')))
        else:
            page_reference=[0]
        frame_size = int(request.form['frame_size'])
        algorithm = request.form['algorithm']
        
        if algorithm == 'fifo':
            page_faults, process_steps = fifo(page_reference, frame_size)
        elif algorithm == 'lru':
            page_faults, process_steps = lru(page_reference, frame_size)
        elif algorithm == 'optimal':
            page_faults, process_steps = optimal(page_reference, frame_size)
        
        return render_template('page.html', page_faults=page_faults, process_steps=process_steps)
    return render_template('page.html')



if __name__=="__main__":
    app.run(debug=True,port=8000)