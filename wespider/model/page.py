#-*- coding:utf-8 -*-

from MySQLdb import IntegrityError

from wespider.store import db_conn
from wespider import config

class Page(object):

	def __init__(self):
		self.id = None
		self.source_page_id = None
		self.page_box_id = None
		self.user_id = None
		self.title = None
		self.url = None
		self.tip = None
		self.date = None
	
	def __repr__(self):
		return "<Page id=%s, title=%s>" % (self.id, self.title)

	__str__ = __repr__
	
	
	
	@classmethod
    	def get(cls, id):
		
		cursor = db_conn.gcae('select id, source_page_id, page_box_id, user_id, title, url, tip, date from page where id=%s' % (id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			pg = cls()
			pg.id = row[0]
			pg.source_page_id = row[1]
			pg.page_box_id = row[2]
			pg.user_id = row[3]
			pg.title = row[4]
			pg.url = row[5]
			pg.tip = row[6]
			pg.date = row[7]
			return pg
		
		return None	
	
	
	@classmethod
    	def getByUrl(cls, title, url, user_id):
		
		cursor = db_conn.gcae('select id, source_page_id, page_box_id, user_id, title, url, tip, date from page where title="%s" and url="%s" and user_id=%s' % (title, url, user_id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			pg = cls()
			pg.id = row[0]
			pg.source_page_id = row[1]
			pg.page_box_id = row[2]
			pg.user_id = row[3]
			pg.title = row[4]
			pg.url = row[5]
			pg.tip = row[6]
			pg.date = row[7]
			return pg
		
		return None	
	
	
	@classmethod
    	def getByUser(cls, user_id=None, start=0, limit=10):
		
		cursor = db_conn.gcae('select id, source_page_id, page_box_id, user_id, title, url, tip, date from page where user_id=%s order by date desc limit %s,%s' % (user_id, start, limit))
		
		data = cursor.fetchall()
	        cursor and cursor.close()
		
		pgs = []

		if data:
			for row in data:
				pg = cls()
				pg.id = row[0]
				pg.source_page_id = row[1]
				pg.page_box_id = row[2]
				pg.user_id = row[3]
				pg.title = row[4]
				pg.url = row[5]
				pg.tip = row[6]
				pg.date = row[7]
				
				pgs.append(pg)
		
		return pgs
	
	
	@classmethod
    	def getByPagebox(cls, pb_id=None, start=0, limit=10):
		
		cursor = db_conn.gcae('select id, source_page_id, page_box_id, user_id, title, url, tip, date from page where page_box_id=%s order by date desc limit %s,%s' % (pb_id, start, limit))
		
		data = cursor.fetchall()
	        cursor and cursor.close()
		
		pgs = []

		if data:
			for row in data:
				pg = cls()
				pg.id = row[0]
				pg.source_page_id = row[1]
				pg.page_box_id = row[2]
				pg.user_id = row[3]
				pg.title = row[4]
				pg.url = row[5]
				pg.tip = row[6]
				pg.date = row[7]
				
				pgs.append(pg)
		
		return pgs


	@classmethod
	def add(cls, source_page_id=None, page_box_id=None, user_id=None, title=None, url=None, tip=None, date=None):
		cursor = None
		page = None
		
		try:
			cursor = db_conn.gcae("""insert into page (source_page_id, page_box_id, user_id, title, url, tip, date) 
						    values (%s, %s, %s, %s, %s, %s, %s)""", (source_page_id, page_box_id, user_id, title, url, tip, date))
		
			pg_id = cursor.lastrowid
			#db_conn.commit()
			page = cls.get(pg_id)
		except IntegrityError:
			print 'IntegrityError at page add'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return page


	def update(self, page_box_id=None, page_title=None, page_tip=None):
		cursor = None
		page = None

		page_box_id = page_box_id or self.page_box_id
		page_title = page_title or self.title
		page_tip = page_tip or self.tip

		try:
			cursor = db_conn.gcae('update page set page_box_id=%s, title="%s", tip="%s" where id=%s' % (page_box_id, page_title, page_tip, self.id))
		
			#db_conn.commit()
			page = self
		except IntegrityError:
			print 'IntegrityError at page update'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return page
	
	
	@classmethod
	def delete(cls, page_id=None):
		cursor = None

		try:
			cursor = db_conn.gcae('delete from page where id=%s' % (page_id))
			#db_conn.commit()
		except IntegrityError:
			print 'IntegrityError at page delete'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return page_id
	
	@classmethod
	def search(cls, pg_skw=None, pb_id=None, user_id=None, start=0, limit=10):
		cursor = None
		
		if pb_id:
			cursor = db_conn.gcae('select id, source_page_id, page_box_id, user_id, title, url, tip, date from page where (title like "%%%s%%" or tip like "%%%s%%") and page_box_id=%s and user_id=%s order by date desc limit %s,%s' % (pg_skw, pg_skw, pb_id, user_id, start, limit))
		else:
			cursor = db_conn.gcae('select id, source_page_id, page_box_id, user_id, title, url, tip, date from page where (title like "%%%s%%" or tip like "%%%s%%") and user_id=%s order by date desc limit %s,%s' % (pg_skw, pg_skw, user_id, start, limit))
		
		data = cursor.fetchall()
	        cursor and cursor.close()
		
		pgs = []

		if data:
			for row in data:
				pg = {}
				pg['id'] = row[0]
				pg['source_page_id'] = row[1]
				pg['page_box_id'] = row[2]
				pg['user_id'] = row[3]
				pg['title'] = row[4]
				pg['url'] = row[5]
				pg['tip'] = row[6]
				pg['date'] = row[7]
				
				pgs.append(pg)
		
		return pgs


