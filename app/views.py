from flask import render_template
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

@app.route('/Register')
def about():
    
    form= RegistrationForm()
    
    return render_template('register.html', title='Register', form=form)

@app.route('/Login')
def about():
    
    form= LoginForm()
    
    return render_template('login.html', title='Register', form=form)