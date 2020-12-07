from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint

import os


auth = Blueprint('auth', __name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = os.urandom(24)
application = app
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
db.create_all()

class posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer(), nullable = False)
    description = db.Column(db.String(200), nullable=False)
    # function to return a string when we add something
    def __repr__(self):
        return '<Name %r>' % self.id

class users(db.Model):
    username = db.Column(db.String(200), primary_key = True)
    password_hash = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    firstname = db.Column(db.String(200), nullable = False)
    lastname = db.Column(db.String(200), nullable = False)
    location = db.Column(db.String(200), nullable = False)
    

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
        # function to return a string when we add something
    def __repr__(self):
        return '<User %r>' % self.username




    


class NameForm(FlaskForm):
    usr = StringField('Enter an Username: ',
                             validators=[DataRequired()])
    loc = StringField('Enter an location: ',
                             validators=[DataRequired()])
    rate = IntegerField('Enter an Rating: ',
                             validators=[DataRequired()])
    desc = StringField('Enter an Description: ',
                             validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    title = "New Post"
    if request.method == "POST":
        u = request.form['usr']
        l = request.form['loc']
        r = request.form['rate']
        d = request.form['desc']
        new_post = posts(username=u, location = l, rating = r, description = d)
        # push to database
        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('create'))
        except:
            return "There was an error adding your post."
    else:
        p = posts.query.order_by(posts.id)
        return render_template('create.html', title=title, create=p)

@app.route("/delete", methods=['GET', "POST"])
def delete():
    title = request.form.get("title")
    post = posts.query.filter_by(location=title).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('profile'))


#Sign-In Route
@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    
    if request.method == "GET":

        u = request.args.get("uname")
        p = request.args.get("psw")
        r = request.args.get("remember")
    
        print("Username: " + u)
        print("Password: " + p)
        print("Remember: " + r)        

        print("GET is successful")

        user = users()

        userExists = db.session.query(users.username).filter_by(username=u).scalar() is not None

        if(userExists):
            user = users.query.filter_by(username=u).first()
        else:
            print("I FAILED TO GET USER")


        if(users.verify_password(self = user, password = p) is not None):
            print("HASH WORKS")
            return redirect(url_for('index', firstName = user.firstname, lastName = user.lastname))
            
        else:
            print("HASH FAILS")
            return redirect(url_for('login'))

    else:
        print("GET IS UNSUCCESFUL")
    

#Sign-up Route
@app.route('/signup', methods = ['GET', 'POST'])
def signup():

    title = "Signup"

    if request.method == "POST":
        f = request.form['fname']
        l = request.form['lname']
        loc = request.form['loc']
        u = request.form['uname']
        p = request.form['psw']
        e = request.form['email']

        emailExists = db.session.query(users.email).filter_by(email=e).scalar() is not None

        if(emailExists):
            flash('The email already exists. Please try again')
            return redirect(url_for('login'))
        
        userExists = db.session.query(users.username).filter_by(username=u).scalar() is not None

        if(userExists):
            flash('The username already exists. Please try again')
            return redirect(url_for('login'))
    
        print("I REACH HERE")
        new_user = users(username = u, password = p, email = e, firstname = f, lastname = l, location = loc)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except: 
            flash("The query failed. Please try again")
            return redirect(url_for('login'))

    else:
        print("Should not reach here; there is no GET for signup")
        us = users.query.order_by(users.username)
        return render_template('login.html', title = title, create = us)

@app.route('/profile')
def profile():
        title = "Posts"
        p = posts.query.order_by(posts.id)
        return render_template('profile.html', title=title, create=p)