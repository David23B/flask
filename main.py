from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'a_very_secret_key_12345'

@app.route('/')
def home():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('front_page.html', username=usnername, student_id=student_id)

@app.route('/my_reservations')
def my_reservations():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('my_reservations.html', username=usnername, student_id=student_id)

@app.route('/room_reservations')
def room_reservations():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('room_reservations.html', username=usnername, student_id=student_id)

@app.route('/room/1')
def room1():
    return render_template('room/1.html')

@app.route('/room/2')
def room2():
    return render_template('room/2.html')

@app.route('/misd_query')
def misd_query():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('misd_query.html', username=usnername, student_id=student_id)

@app.route('/my_reservations/slot')
def slot():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('my_reservations/slot.html', username=usnername, student_id=student_id)

@app.route('/my_reservations/slot2')
def slot2():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('my_reservations/slot2.html', username=usnername, student_id=student_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['student_id'] = request.form['student_id']
        return redirect(url_for('room1'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
   
