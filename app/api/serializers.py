# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Time    : 17/3/19 下午11:21
# @Author  : robinjia
# @Email   : dengshilong1988@gmail.com
from flask_marshmallow import Marshmallow
from marshmallow import fields

from app.models import Post, User, Category

ma = Marshmallow()


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User


class CategorySchema(ma.ModelSchema):

    class Meta:
        model = Category


class PostSchema(ma.ModelSchema):
    author = fields.Nested(UserSchema, only=["username"])
    category = fields.Nested(CategorySchema, only=["name"])

    class Meta:
        model = Post


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
