# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Time    : 17/2/28 下午2:59
# @Author  : robinjia
# @Email   : dengshilong1988@gmail.com
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    category = StringField(validators=[DataRequired(), Length(1, 64),])
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('提交')
