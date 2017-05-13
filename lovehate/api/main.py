# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Time    : 17/3/17 上午11:42
# @Author  : robinjia
# @Email   : dengshilong1988@gmail.com
from flask import Blueprint
from flask_restful import Resource, Api

from ..models import Category, Post
from .serializers import posts_schema
api_bp = Blueprint('api', __name__)
API = Api(api_bp)


class CategoryPostAPI(Resource):

    def get(self, category):
        category = Category.query.filter_by(name=category).first_or_404()
        posts = Post.query.filter_by(
            category_id=category.id).order_by(Post.create_time.desc())
        return posts_schema.jsonify(posts)


class HelloWorld(Resource):

    def get(self):
        return {'hello': 'world'}


API.add_resource(CategoryPostAPI, '/category/<string:category>')
API.add_resource(HelloWorld, '/test')
