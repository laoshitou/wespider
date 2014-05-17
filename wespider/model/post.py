#-*- coding:utf-8 -*-

from MySQLdb import IntegrityError

from wespider.store import db_conn
from wespider import config

class Post(object):

	def __init__(self):
		self.id = None
		self.column_id = None
		self.title = None
		self.content = None
		self.excerpt = None
		self.commit_content = None
		self.user_id = None
		self.update_date = None
		self.visibility = None
	
	def __repr__(self):
		return "<Post id=%s, title=%s>" % (self.id, self.title)

	__str__ = __repr__
	
	
	
	@classmethod
    	def get(cls, id):
		
		cursor = db_conn.gcae('select id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id from post where id=%s' % (id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			pt = cls()
			pt.id = row[0]
			pt.column_id = row[1]
			pt.title = row[2]
			pt.content = row[3]
			pt.excerpt = row[4]
			pt.commit_content = row[5]
			pt.update_date = row[6]
			pt.visibility = row[7]
			pt.user_id = row[8]
			return pt
		
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
		
		cursor = db_conn.gcae('select id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id from post where user_id=%s order by update_date desc limit %s,%s' % (user_id, start, limit))
		
		data = cursor.fetchall()
	        cursor and cursor.close()
		
		pts = []

		if data:
			for row in data:
				pt = cls()
				pt.id = row[0]
				pt.column_id = row[1]
				pt.title = row[2]
				pt.content = row[3]
				pt.excerpt = row[4]
				pt.commit_content = row[5]
				pt.update_date = row[6]
				pt.visibility = row[7]
				pt.user_id = row[8]

				pts.append(pt)

		return pts
	
	
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
	def add(cls, column_id=None, title=None, content=None, excerpt=None, commit_content=None, update_date=None, visibility=None, user_id=None):
		cursor = None
		post = None
	
		try:
			cursor = db_conn.gcae("""insert into post (column_id, title, content, excerpt, commit_content, update_date, visibility, user_id) 
						    values (%s, %s, %s, %s, %s, %s, %s, %s)""", 
						    (column_id, title, content, excerpt, commit_content, update_date, visibility, user_id))
		
			post_id = cursor.lastrowid
			#db_conn.commit()
			post = cls.get(post_id)
		except IntegrityError:
			print 'IntegrityErrot post add'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return post


	def update(self, column_id=None, title=None, content=None, excerpt=None, commit_content=None, update_date=None, visibility=None):
		cursor = None
		post = None

		column_id = column_id or self.column_id
		title = title or self.title
		content = content or self.content
		content = content.replace("'","\\'")
		excerpt = excerpt or self.excerpt
		excerpt = excerpt.replace("'","\\'")
		commit_content = commit_content or self.commit_content
		update_date = update_date or self.update_date
		visibility = visibility or self.visibility

		try:
			cursor = db_conn.gcae("""update post set column_id=%s, title='%s', content='%s', excerpt='%s', commit_content='%s', update_date='%s', visibility='%s' where id=%s""" % (column_id, title, content, excerpt, commit_content, update_date, visibility, self.id))
		
			#db_conn.commit()
			post = self
		except IntegrityError:
			print 'IntegrityError at post update'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return post
	
	
	@classmethod
	def Delete(cls, post_id=None):
		cursor = None

		try:
			cursor = db_conn.gcae('delete from post where id=%s' % (post_id))
			#db_conn.commit()
		except IntegrityError:
			print 'IntegrityError at post Delete'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return post_id
	
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


