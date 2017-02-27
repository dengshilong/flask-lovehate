from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from werkzeug.security import generate_password_hash

from app.auth.forms import LoginForm, RegisterForm
from . import auth
from .. import db
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('邮箱或密码错误.')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('邮箱已注册')
        user = User.query.filter_by(email=form.username.data).first()
        if user:
            flash('昵称已注册')
        user = User(email=form.email.data, username=form.username.data,
                    password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        redirect('auth.login')
    return render_template('auth/register.html', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('你已登出')
    return redirect(url_for('main.index'))



@auth.route('/reset', methods=['GET'])
def password_reset_request():
    return None