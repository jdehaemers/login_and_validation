from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login():
    login_errors = {'Invalid password', 'Invalid email'}
    return render_template('login.html', login_errors=login_errors)

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/login')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'], 
        'last_name' : request.form['last_name'], 
        'email' : request.form['email'],
        'password': pw_hash
        }
    user_id = User.create(data)
    session['user_id'] = user_id
    session['logged_in'] = True
    return redirect('/success')

@app.route('/success')
def success():
    if 'logged_in' not in session:
        return redirect('/')
    return render_template('success.html')

@app.route('/login/user', methods=['POST'])
def login_user():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
        }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid email')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db['password'], request.form['password']):
        flash('Invalid password')
        return redirect('/login')
    session['user_id'] = user_in_db['id']
    session['logged_in'] = True
    return redirect('/success')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/login')