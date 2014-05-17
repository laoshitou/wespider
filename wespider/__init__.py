#-*- coding:utf-8 -*-

from flask import Flask
from flask import render_template

app = Flask(__name__)

app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


import views
