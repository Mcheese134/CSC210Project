from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
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

@app.route('/profile')
def profile():
        title = "Posts"
        p = posts.query.order_by(posts.id)
        return render_template('profile.html', title=title, create=p)



  