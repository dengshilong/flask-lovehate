# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Time    : 17/2/28 下午2:47
# @Author  : robinjia
# @Email   : dengshilong1988@gmail.com

import uuid
from datetime import datetime
import os
from manage import app

def get_uuid_filename(filename):
    folder = os.path.join(app.config['UPLOAD_DIR'], datetime.now().strftime("%Y/%m/%d"))
    if not os.path.exists(folder):
        os.makedirs(folder)
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(folder, filename)