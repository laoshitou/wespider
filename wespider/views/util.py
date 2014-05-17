#-*- coding:utf-8 -*-

from functools import wraps

from flask import g, flash, redirect, url_for, abort
from flask import render_template
from flask import jsonify


def require_login(msg="", flash_sign=False, title=""):
	def _(f):
		@wraps(f)
		def __(*a, **kw):
			if not g.user:

				error_msg = msg or u"未登录用户，无法进行本操作"
				
				if flash_sign:
					flash(error_msg, 'error')
					return render_template('access_denied.html', title=title, content=error_msg)

				return jsonify(success=False, nologin=True, tip=error_msg)
			return f(*a, **kw)
		return __
	return _
