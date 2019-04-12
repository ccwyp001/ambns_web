# -*- coding: utf-8 -*-

import hashlib

def md5_code(text):
    md = hashlib.md5()
    md.update(text.encode())
    return md.hexdigest().upper()