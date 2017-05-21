# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Time    : 17/2/28 下午2:47
# @Author  : robinjia
# @Email   : dengshilong1988@gmail.com

import uuid
from datetime import datetime
import os
import math

from PIL import Image
from flask import current_app

from lovehate import db
from lovehate.models import Category


def get_uuid_filename(filename):
    folder = datetime.now().strftime("%Y/%m/%d")
    path = os.path.join(current_app.config['STATIC_BASE_DIR'], current_app.config[
                        'UPLOAD_DIR'], folder)
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(current_app.config['STATIC_BASE_DIR'], current_app.config[
                        'THUMBNAIL_DIR'], folder)
    if not os.path.exists(path):
        os.makedirs(path)
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(folder, filename)


def generate_thumbnail(filename):
    origin = os.path.join(current_app.config['STATIC_BASE_DIR'], current_app.config[
                          'UPLOAD_DIR'], filename)
    outfile = os.path.join(current_app.config['STATIC_BASE_DIR'], current_app.config[
                           'THUMBNAIL_DIR'], filename)
    folder = '/'.join(outfile.split('/')[:-1])
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        im = Image.open(origin)
        if im.size[0] * im.size[1] <= current_app.config['THUMBNAIL_THRESHOLD']:
            return
        rate = im.size[0] * im.size[1] / \
            current_app.config['THUMBNAIL_THRESHOLD']
        size = (im.size[0] / math.sqrt(rate), im.size[1] / math.sqrt(rate))
        im.thumbnail(size)
        if hasattr(im, '_getexif'):
            exif = im._getexif()  # pylint: disable=protected-access
            if exif and exif.get(274, 1) == 6:  # 如果是横着的照片
                im = im.transpose(Image.ROTATE_270)
        im.save(outfile)
    except IOError as error:
        print("cannot create thumbnail for", origin)
        print(error)


def get_default_category():
    default = '无题'
    category = Category.query.filter_by(name=default).first()
    if not category:
        category = Category(name=default)
        db.session.add(category)
        db.session.commit()
    return category
