from flask import render_template, request, url_for, flash, redirect
from pitch import app, db
from pitch.forms import RegistrationForm, LoginForm, UpdateForm
from pitch.models import User, Pitch
from flask_login import login_user, current_user,login_required, logout_user 





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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = User.query.filter_by(password=form.password.data).first()
        if user and password:
            login_user(user, remember=form.remember.data)
            flash('Login Successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username or password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated Successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)