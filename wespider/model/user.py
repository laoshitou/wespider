#-*- coding:utf-8 -*-

from MySQLdb import IntegrityError

from wespider.store import db_conn
from wespider import config

class User(object):

	def __init__(self):
		self.id = None
		self.user_name = None
		self.user_email = None
		self.real_name = None
		self.password = None
		self.status = None
		self.session_id = None
		self.avatar_big_url = None
		self.avatar_mid_url = None
		self.avatar_small_url = None
	
	def __repr__(self):
		return "<User id=%s, user_name=%s>" % (self.id, self.user_name)

	__str__ = __repr__
	
	
	@classmethod
    	def verify(cls, user_email_name, password):
		
		cursor = db_conn.gcae('select id, user_name, password, user_email, real_name from user where (user_name="%s" or user_email="%s") and password="%s"' % (user_email_name, user_email_name, password))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			u = cls()
			u.id = row[0]
			u.user_name = row[1]
			u.password = row[2]
			u.user_email = row[3]
			u.real_name = row[4]
			return u
		
		return None	

	
	@classmethod
    	def get(cls, id):
		
		cursor = db_conn.gcae('select id, user_name, password, user_email, real_name from user where id=%s' % (id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			u = cls()
			u.id = row[0]
			u.user_name = row[1]
			u.password = row[2]
			u.user_email = row[3]
			u.real_name = row[4]
			return u
		
		return None	
	
	
	@classmethod
    	def getBySessionid(cls, session_id):
		cursor = db_conn.gcae("""select id, user_name, password, user_email, real_name from user where session_id='%s'""" % (session_id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			u = cls()
			u.id = row[0]
			u.user_name = row[1]
			u.password = row[2]
			u.user_email = row[3]
			u.real_name = row[4]
			return u
		
		return None	

	@classmethod
    	def getByName(cls, user_name):
		
		cursor = db_conn.gcae("""select id, user_name, password, user_email, real_name from user where user_name='%s'""" % (user_name))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			u = cls()
			u.id = row[0]
			u.user_name = row[1]
			u.password = row[2]
			u.user_email = row[3]
			u.real_name = row[4]
			return u
		
		return None	

	@classmethod
    	def getByEmail(cls, user_email):
		
		cursor = db_conn.gcae("""select id, user_name, password, user_email, real_name from user where user_email='%s'""" % (user_email))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			u = cls()
			u.id = row[0]
			u.user_name = row[1]
			u.password = row[2]
			u.user_email = row[3]
			u.real_name = row[4]
			return u
		
		return None	


	@classmethod
	def add(cls, user_name=None, password=None, user_email=None):
		cursor = None
		user = None

		user_name = "" if user_name is None else user_name
		password = "" if password is None else password
		
		try:
			cursor = db_conn.gcae("""insert into user (user_name, user_email, password) 
						    values (%s, %s, %s)""", (user_name, user_email, password))
		
			user_id = cursor.lastrowid
			#db_conn.commit()
			user = cls.get(user_id)
		except IntegrityError:
			#db_conn.rollback()
			print 'IntegrityError at user add'
		finally:
			cursor and cursor.close()

		return user


	def update_session(self, session_id):
		cursor = db_conn.gcae("""update user set session_id='%s' where id=%s""" % (session_id, self.id))
		#db_conn.commit()
		cursor and cursor.close()

	def clear_session(self):
		self.update_session("")

