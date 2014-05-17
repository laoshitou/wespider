#-*- coding:utf-8 -*-

import os
import commands
import datetime

import MySQLdb


import config


def init_db():
	cmd = """mysql -h%s -P%s -u%s -p%s %s< %s""" \
			% (config.DB_HOST, config.DB_PORT, config.DB_USER, config.DB_PASSWD, config.DB_NAME, os.path.join(os.path.dirname(__file__), "schema.sql"))
	
	status, output = commands.getstatusoutput(cmd)

	if status != 0:
		print "init_db fail, output is: %s" % output
		return status



def connect_db():
	try:
		conn = MySQLdb.connect(
				host = config.DB_HOST,
				port =config.DB_PORT,
				user = config.DB_USER,
				passwd = config.DB_PASSWD,
				db = config.DB_NAME,
				use_unicode=True,
				charset="utf8")
		return conn
	except Exception, e:
		print "connect db fail:%s" % e
		return None



class DB(object):

	def __init__(self):
		self._conn = None
		self._conn = connect_db()

	def connect(self):
		self._conn = connect_db()
		return self._conn

	def gcae(self, *a, **kw):
		cursor = kw.pop('cursor', None)
		try:
			#self._conn or self.connect()
			cursor = cursor or self._conn.cursor()
			cursor.execute(*a)
		except (AttributeError, MySQLdb.OperationalError):
			print 'debug, %s re-connect to mysql' % datetime.datetime.now()
		
			self._conn and self._conn.close()
		
			self.connect()
			cursor = self._conn.cursor()
			cursor.execute(*a)
		
		return cursor

	def commit(self):
		return self._conn and self._conn.commit()

	def rollback(self):
		return self._conn and self._conn.rollback()


db_conn = DB()
