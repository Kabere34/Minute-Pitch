from flask import flash, render_template, redirect, url_for
from app import app
from .forms import RegistrationForm, LoginForm

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
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form= LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'sirgama@protonmail.ch' and form.password.data == '1111':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username or password!', 'danger')
    return render_template('login.html', title='Register', form=form)