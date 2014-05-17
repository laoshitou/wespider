#-*- coding:utf-8 -*-
import os
import re
import time
import datetime
import imghdr
import mimetypes
import random
import string


def randbytes(prefix_str, bytes_):
	return ''.join(random.sample(prefix_str + string.ascii_letters + string.digits, bytes_))
