import os
import secrets
from flask import abort, render_template, request, url_for, flash, redirect
from pitch import app, db
from pitch.forms import PitchForm, RegistrationForm, LoginForm, UpdateForm
from pitch.models import User, Pitch
from flask_login import login_user, current_user,login_required, logout_user 







# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    pitches = Pitch.query.all()
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
    
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


@app.route('/pitch/new', methods=['GET', 'POST'])
@login_required
def new_pitch():
    form = PitchForm()
    
    if form.validate_on_submit():
        pitch = Pitch(title=form.title.data, content=form.content.data,  author=current_user )
        db.session.add(pitch)
        db.session.commit()
        flash('Pitch Created Successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_pitch.html', title='New Pitch', form=form, legend='Update Post')

@app.route('/pitch/<int:pitch_id>')
@login_required
def pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    return render_template('pitch.html', pitch=pitch)
    
    
@app.route('/pitch/<int:pitch_id>/update',methods=['GET', 'POST'])
@login_required
def update_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if pitch.author != current_user:
        abort(403)
        
    form = PitchForm()
    if form.validate_on_submit():
        pitch.title = form.title.data
        pitch.content = form.content.data
        db.session.commit()
        flash('Pitch Updated', 'success')
        return redirect(url_for('pitch', pitch_id=pitch.id))
    elif request.method == "GET":
        form.title.data = pitch.title
        form.content.data = pitch.content
    return render_template('create_pitch.html', form=form, legend='Update Post')
    

@app.route('/pitch/<int:pitch_id>/delete',methods=['POST'])
@login_required
def delete_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if pitch.author != current_user:
        abort(403)
    db.session.delete(pitch)
    db.session.commit()
    flash('Pitch Deleted', 'success')
    return redirect(url_for('index'))