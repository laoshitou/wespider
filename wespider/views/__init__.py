#-*- coding:utf-8 -*-

from flask import session, g, request

from wespider import app
from wespider.model.user import User
import views


@app.before_request
def before_request():
	g.user = None
	print "URL: <%s> before request" % (request.url)
	if session.has_key('session_id'):
		user = User.getBySessionid(session['session_id'])
		g.user = user


