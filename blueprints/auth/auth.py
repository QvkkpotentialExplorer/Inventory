from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, current_user

from data.db_session import create_engine_and_session
from data.user import User
from form.login_form import LoginForm
from form.register_form import RegisterForm
from data.db_session import db_sess
auth_pages = Blueprint('auth_page', __name__, template_folder='../templates', static_folder='static', url_prefix='/auth/')

@auth_pages.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile_page.user'))
    form = RegisterForm()
    if form.validate_on_submit():
        print('Я туту')
        user = User(
            username = form.username.data,
            full_name=form.fullname.data,
            role='user'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for('auth_page.login'))
    return render_template('register.html', form=form)


@auth_pages.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile_page.user'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        print(user)
        login_user(user, remember=form.remember_me.data)
        return redirect(location=url_for('profile_page.user'))

    return render_template('login.html', form=form)


@auth_pages.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')