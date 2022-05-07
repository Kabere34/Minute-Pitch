from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm




app = Flask(__name__)
app.config['SECRET_KEY'] = '564648sjdhbfl654684adfa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    pitches = db.relationship('Pitch', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Pitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Pitch('{self.title}', '{self.date_posted}')"

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


if __name__ == '__main__':
    app.run(debug = True)