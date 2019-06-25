from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt

from mysql_db import connectToMySQL
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "keep it secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/signin')
def buddy_SignIn():
    return redirect('/welcome')

@app.route('/signup')
def buddy_SignUp():
    return render_template('signup.html')

@app.route('/signinprocess')
def buddy_Signinprocess():
    return redirect('/welcome')

@app.route('/signupprocess')
def buddy_Signupprocess():
    return redirect('/welcome')

@app.route('/welcome')
def buddy_Welcome():
    return render_template('userprofile.html')

if __name__ == "__main__":
    app.run(debug=True)