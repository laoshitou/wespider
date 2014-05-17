#-*- coding:utf-8 -*-

from MySQLdb import IntegrityError

from wespider.store import db_conn
from wespider import config

class PostCommit(object):

	def __init__(self):
		self.id = None
		self.post_id = None
		self.column_id = None
		self.title = None
		self.content = None
		self.excerpt = None
		self.commit_content = None
		self.user_id = None
		self.update_date = None
		self.visibility = None
	
	def __repr__(self):
		return "<PostCommit id=%s, title=%s>" % (self.id, self.title)

	__str__ = __repr__
	
	
	
	@classmethod
    	def get(cls, id):
		
		cursor = db_conn.gcae('select id, post_id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id from post_commit where id=%s' % (id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			pc = cls()
			pc.id = row[0]
			pc.post_id = row[1]
			pc.column_id = row[2]
			pc.title = row[3]
			pc.content = row[4]
			pc.excerpt = row[5]
			pc.commit_content = row[6]
			pc.update_date = row[7]
			pc.visibility = row[8]
			pc.user_id = row[9]
			return pc
		
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
		
		cursor = db_conn.gcae('select id, post_id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id from post_commit where user_id=%s order by update_date desc limit %s,%s' % (user_id, start, limit))
		
		data = cursor.fetchall()
	        cursor and cursor.close()
		
		pcs = []

		if data:
			for row in data:
				pc = cls()
				pc.id = row[0]
				pc.post_id = row[1]
				pc.column_id = row[2]
				pc.title = row[3]
				pc.content = row[4]
				pc.excerpt = row[5]
				pc.commit_content = row[6]
				pc.update_date = row[7]
				pc.visibility = row[8]
				pc.user_id = row[9]

				pcs.append(pc)

		return pcs
	
	
	@classmethod
    	def getByPost(cls, post_id=None, start=0, limit=10):
		
		cursor = db_conn.gcae('select id, post_id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id from post_commit where post_id=%s order by update_date desc limit %s,%s' % (post_id, start, limit))
		
		data = cursor.fetchall()
	        cursor and cursor.close()
		
		pcs = []

		if data:
			for row in data:
				pc = cls()
				pc.id = row[0]
				pc.post_id = row[1]
				pc.column_id = row[2]
				pc.title = row[3]
				pc.content = row[4]
				pc.excerpt = row[5]
				pc.commit_content = row[6]
				pc.update_date = row[7]
				pc.visibility = row[8]
				pc.user_id = row[9]

				pcs.append(pc)

		return pcs

	
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
	def add(cls, post_id=None, column_id=None, title=None, content=None, excerpt=None, commit_content=None, update_date=None, visibility=None, user_id=None):
		cursor = None
		post_commit = None
	
		try:
			cursor = db_conn.gcae("""insert into post_commit (post_id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id) 
						    values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
						    (post_id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id))
		
			post_commit_id = cursor.lastrowid
			#db_conn.commit()
			post_commit = cls.get(post_commit_id)
		except IntegrityError:
			print 'IntegrityErrot post_commit add'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return post_commit


		
	
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
	def DeleteByPost(cls, post_id=None):
		cursor = None

		try:
			cursor = db_conn.gcae('delete from post_commit where post_id=%s' % (post_id))
			#db_conn.commit()
		except IntegrityError:
			print 'IntegrityError at post_commit DeleteByPost'
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


