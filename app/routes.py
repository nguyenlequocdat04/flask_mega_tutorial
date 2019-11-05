from app import app
from flask import render_template, flash, redirect, url_for
from app.forms.login import LoginForm
from model.user import UserDAO
from services.user import UserService
from flask_login import current_user, login_user, logout_user


@app.route('/')
@app.route('/index')
def index():
    # print(app.config['SECRET_KEY'])
    # if not current_user:
    #     flash("Please login!!")
    #     return redirect(url_for("login"))
    
    user = {'username': 'dat'}
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
    return render_template('index.html', title = "Home", user = user, posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))

        user = UserService.login(form.username.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_user')
def create_user():
    UserDAO.create_sample_user('datnlq1', '123456')
    return "Ok"

@app.route('/get_all')
def get_all():
    datas = UserService.get_all()
    print(list(datas))
    return "OK"