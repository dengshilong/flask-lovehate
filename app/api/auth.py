# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Time    : 17/3/17 下午6:01
# @Author  : robinjia
# @Email   : dengshilong1988@gmail.com

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api.auth', __name__)
API = Api(api_bp)
