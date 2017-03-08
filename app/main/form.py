# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Time    : 17/2/28 下午2:59
# @Author  : robinjia
# @Email   : dengshilong1988@gmail.com
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length


class PostForm(FlaskForm):
    category = StringField()
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('提交')


class EditProfileForm(FlaskForm):
    # avatar = FileField('头像')
    location = StringField('城市', validators=[Length(0, 64)])
    about_me = TextAreaField('个人介绍')
    submit = SubmitField('提交')
