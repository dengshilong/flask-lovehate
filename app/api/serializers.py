# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Time    : 17/3/19 下午11:21
# @Author  : robinjia
# @Email   : dengshilong1988@gmail.com
from flask_marshmallow import Marshmallow

from app.models import Post

ma = Marshmallow()


class PostSchema(ma.ModelSchema):

    class Meta:
        model = Post


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
