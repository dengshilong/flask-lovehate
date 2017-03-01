# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Time    : 17/2/28 下午2:47
# @Author  : robinjia
# @Email   : dengshilong1988@gmail.com

import uuid
from datetime import datetime
import os

from flask import current_app

from app import db
from app.models import Category


def get_uuid_filename(filename):
    folder = os.path.join(
        current_app.config['UPLOAD_DIR'], datetime.now().strftime("%Y/%m/%d"))
    path = os.path.join(current_app.config['STATIC_BASE_DIR'], folder)
    if not os.path.exists(path):
        os.makedirs(path)
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(folder, filename)


def get_default_category():
    default = '无题'
    category = Category.query.filter_by(name=default).first()
    if not category:
        category = Category(name=default)
        db.session.add(category)
        db.session.commit()
    return category
