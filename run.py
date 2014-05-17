#-*- coding:utf-8 -*-

import os

activate_this = '%s/venv/bin/activate_this.py' % os.path.dirname(os.path.abspath(__file__))
execfile(activate_this, dict(__file__=activate_this))

from werkzeug.contrib.fixers import ProxyFix
from wespider import app
app.wsgi_app = ProxyFix(app.wsgi_app)
app.debug = True
app.config['SITE_NAME'] = "WeSpider"


if __name__ == "__main__":
	app.debug = True
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(host="115.29.224.99",port=8333)
