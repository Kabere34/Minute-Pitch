from flask import render_template, url_for, flash, redirect
from pitch import app, db
from pitch.forms import RegistrationForm, LoginForm
from pitch.models import User, Pitch
from flask_login import login_user





pitches = [
    {
        'author': 'Gamaliel',
        'title' : 'Igniting Interest',
        'content' : 'sample cont 1',
        'category' : 'business',
        'date_posted': 'May 6th 2022'      
      
    },
    {
        'author': 'Gamaliel',
        'title' : 'Igniting Interest',
        'content' : 'sample cont 1',
        'category' : 'business',
        'date_posted': 'May 6th 2022'      
    
    }
]

# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html', pitches = pitches)

@app.route('/about')
def about():
    
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    form= RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = User.query.filter_by(password=form.password.data).first()
        if user and password:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash('Login unsuccessful. Please check your username or password!', 'danger')
    return render_template('login.html', title='Register', form=form)
