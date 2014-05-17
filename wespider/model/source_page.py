#-*- coding:utf-8 -*-

from MySQLdb import IntegrityError

from wespider.store import db_conn
from wespider import config

class SourcePage(object):

	def __init__(self):
		self.id = None
		self.title = None
		self.url = None
	
	def __repr__(self):
		return "<Page id=%s, title=%s>" % (self.id, self.title)

	__str__ = __repr__
	
	
	
	@classmethod
    	def get(cls, id):
		
		cursor = db_conn.gcae('select id, title, url from source_page where id=%s' % (id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			s_pg = cls()
			s_pg.id = row[0]
			s_pg.title = row[1]
			s_pg.url = row[2]
			return s_pg
		
		return None	
	
	
	@classmethod
    	def getByUrl(cls, url):
		
		cursor = db_conn.gcae('select id, title, url from source_page where url="%s"' % (url))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			s_pg = cls()
			s_pg.id = row[0]
			s_pg.title = row[1]
			s_pg.url = row[2]
			return s_pg
		
		return None	
	
	
	
	@classmethod
	def add(cls, title=None, url=None):
		cursor = None
		source_page = None
		
		try:
			cursor = db_conn.gcae("""insert into source_page (title, url) 
						    values (%s, %s)""", (title, url))
		
			s_pg_id = cursor.lastrowid
			db_conn.commit()
			source_page = cls.get(s_pg_id)
		except IntegrityError:
			db_conn.rollback()
		finally:
			cursor and cursor.close()

		return source_page



