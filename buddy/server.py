from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_bcrypt import Bcrypt

from mysql_db import connectToMySQL
import re
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "keep it secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# ---------------------------------------------------
@app.route('/')
def root():
    return render_template('index.html')

# route to process new registration
@app.route('/signupprocess', methods=['POST'])
def signup():

    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!", 'email')

    query = "SELECT * FROM users WHERE email = %(email)s"
    data = {
        'email': request.form['email']
    }
    mysql = connectToMySQL('buddy')
    results = mysql.query_db(query, data)
    print(results)

    # form validations
    if len(results) > 0:
        is_valid = False
        flash("Email already registered", 'email')

    if len(request.form['first_name']) < 1:
        is_valid = False
        flash("Must provide a first name.", 'first_name')

    if len(request.form['last_name']) < 1:
        is_valid = False
        flash("Must provide a last name.", 'last_name')

    if len(request.form['pronoun']) < 1:
        is_valid = False
        flash("Please provide your preferred pronoun.", 'pronoun')

    if len(request.form['about']) < 1:
        is_valid = False
        flash("Please share a short bio about yourself!", 'about')

    if len(request.form['password']) < 8:
        is_valid = False
        flash("Your password must be at least 8 characters.", 'password')

    if not request.form['password'] == request.form['password_confirmation']:
        is_valid = False
        flash("Passwords don't match.", 'password')

    if len(request.form['telephone']) < 10:
        is_valid = False
        flash("10-digit phone number required.", 'telephone')

    if not is_valid:
        return redirect('/signup')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        mysql = connectToMySQL('buddy')
        query = "INSERT INTO users (first_name, last_name, pronoun, about, email, telephone, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(pronoun)s, %(about)s, %(email)s, %(telephone)s, %(password)s, NOW(), NOW());"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'pronoun': request.form['pronoun'],
            'about': request.form['about'],
            'email': request.form['email'],
            'telephone': request.form['telephone'],
            'password': pw_hash
        }
        id = mysql.query_db(query, data)
        print(id)
        session['userid'] = id
        return redirect('/welcome')

# login route for returning members
@app.route('/signin', methods=['POST'])
def member():

    if 'userid' not in session:
        flash('You are not logged in', 'member')
        return redirect('/')

    mysql = connectToMySQL('buddy')
    query = "SELECT password, id FROM users WHERE email = %(email)s;"
    data = {
        'email': request.form['email'],
    }
    mysql = connectToMySQL('buddy')
    results = mysql.query_db(query, data)

    if len(results) > 0:
        if bcrypt.check_password_hash(results[0]['password'], request.form['password']):
            session['userid'] = results[0]['id']
            return redirect('/welcome')
        else:
            flash("Invalid email or password", 'member')
            return redirect('/')
    else:
        flash("Invalid email or password", 'member')
        return redirect('/')


# route to render page to create new account
@app.route('/signup')
def signin_process():
    return render_template('signup.html')

@app.route('/email', methods=['POST'])
def email():
    print("In email ajax post route.."*80)
    found = False
    mysql = connectToMySQL('buddy')
    query = "SELECT email from users WHERE users.email = %(email)s;"
    data = { 'email': request.form['email'] }
    result = mysql.query_db(query, data)
    print('ajax process working')
    if result:
        found = True
    return render_template("email.html", found = found)


@app.route('/welcome')
def buddy_Welcome():

    if 'userid' not in session:
        flash('You are not logged in', 'member')
        return redirect('/')

    userid = session['userid']

    mysql = connectToMySQL('buddy')
    user_query = "SELECT * FROM users WHERE id=" +str(userid)
    users = mysql.query_db(user_query)
    return render_template('userprofile.html', users=users)


@app.route('/available')
def accepted():

    if 'userid' not in session:
        flash('You are not logged in', 'member')
        return redirect('/')

    # return render_template('accepted.html')
    userid = session['userid']
    mysql = connectToMySQL('buddy')
    query = "SELECT first_name FROM users WHERE id=" +str(userid)
    first_name = mysql.query_db(query)

    mysql = connectToMySQL('buddy')
    query = "SELECT about FROM users WHERE id=" +str(userid)
    about = mysql.query_db(query)

    return render_template('accepted.html', first_name=first_name, about=about)


@app.route('/review', methods=['POST'])
def review():

    if 'userid' not in session:
        flash('You are not logged in', 'member')
        return redirect('/')

    userid = session['userid']
    mysql = connectToMySQL('buddy')
    query = "INSERT INTO reviews (message, reviewer_id, updated_at, created_at) VALUES (%(message)s, %(reviewer_id)s, NOW(), NOW());"
    data = {
        'message': request.form['message'],
        'reviewer_id': userid
    }
    mysql.query_db(query, data)
    flash("Thank you for your review!", 'review')
    return redirect('/welcome')



@app.route('/location')
def location():
    
    if 'userid' not in session:
        flash('You are not logged in', 'member')
        return redirect('/')
    return render_template('location.html')

if __name__ == "__main__":
    app.run(debug=True)
