activate_this = '/data/webapps/wespider/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


import sys
sys.path.insert(0, '/data/wespider/wespider')

from wespider import app as application
