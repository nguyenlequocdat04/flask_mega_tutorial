from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms.login import LoginForm
from app.forms.register import RegistrationForm
from services.user import UserService
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import json
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    # print(app.config['SECRET_KEY'])
    if not current_user:
        flash("Please login!!")
        return redirect(url_for("login"))
    
    user = {'username': 'Stranger'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title = "Home", posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))

        user = UserService.login(form.username.data, form.password.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/get_all')
@login_required
def get_all():
    datas = UserService.get_all()
    
    return jsonify(list(datas))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # create user
        create_user = UserService.create_user(form.username.data, form.password.data, form.email.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = UserService.get_by_username(username)
    if user:
        posts = [
            {'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}
        ]
        return render_template('user.html', user=user, posts=posts)
    return 'Not found user'