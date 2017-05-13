from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(
        '邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    email = StringField(
        '邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('昵称', validators=[DataRequired(), Length(1, 64), ])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('再次输入密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('昵称已被注册')


class PasswordResetRequestForm(FlaskForm):
    email = StringField(
        '邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('重置密码')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), Length(1, 64), Email()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='两次密码必须相同')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('未知的邮箱')
