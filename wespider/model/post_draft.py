#-*- coding:utf-8 -*-

from MySQLdb import IntegrityError

from wespider.store import db_conn
from wespider import config

class PostDraft(object):

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
		return "<PostDraft id=%s, title=%s>" % (self.id, self.title)

	__str__ = __repr__
	
	
	
	@classmethod
    	def get(cls, id):
		
		cursor = db_conn.gcae('select id, post_id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id from post_draft where id=%s' % (id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			pd = cls()
			pd.id = row[0]
			pd.post_id = row[1]
			pd.column_id = row[2]
			pd.title = row[3]
			pd.content = row[4]
			pd.excerpt = row[5]
			pd.commit_content = row[6]
			pd.update_date = row[7]
			pd.visibility = row[8]
			pd.user_id = row[9]
			return pd
		
		return None	


	@classmethod
    	def getByPost(cls, post_id):
		
		cursor = db_conn.gcae('select id, post_id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id from post_draft where post_id=%s' % (post_id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			pd = cls()
			pd.id = row[0]
			pd.post_id = row[1]
			pd.column_id = row[2]
			pd.title = row[3]
			pd.content = row[4]
			pd.excerpt = row[5]
			pd.commit_content = row[6]
			pd.update_date = row[7]
			pd.visibility = row[8]
			pd.user_id = row[9]
			return pd
		
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
		
		cursor = db_conn.gcae('select id, post_id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id from post_draft where user_id=%s order by update_date desc limit %s,%s' % (user_id, start, limit))
		
		data = cursor.fetchall()
	        cursor and cursor.close()
		
		pds = []

		if data:
			for row in data:
				pd = cls()
				pd.id = row[0]
				pd.post_id = row[1]
				pd.column_id = row[2]
				pd.title = row[3]
				pd.content = row[4]
				pd.excerpt = row[5]
				pd.commit_content = row[6]
				pd.update_date = row[7]
				pd.visibility = row[8]
				pd.user_id = row[9]

				pds.append(pd)

		return pds
	
	
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
		post_draft = None
	
		try:
			cursor = db_conn.gcae("""insert into post_draft (post_id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id) 
						    values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
						    (post_id, column_id, title, content, excerpt, commit_content, update_date, visibility, user_id))
		
			post_draft_id = cursor.lastrowid
			#db_conn.commit()
			post_draft = cls.get(post_draft_id)
		except IntegrityError:
			print 'IntegrityErrot post_draft add'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return post_draft


	def update(self, column_id=None, title=None, content=None, excerpt=None, commit_content=None, update_date=None, visibility=None):
		cursor = None
		post_draft = None

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
			print """update post_draft set column_id=%s, title='%s', content='%s', excerpt='%s', commit_content='%s', update_date='%s', vis    ibility='%s' where id=%s""" % (column_id, title, content, excerpt, commit_content, update_date, visibility, self.id)

			cursor = db_conn.gcae("""update post_draft set column_id=%s, title='%s', content='%s', excerpt='%s', commit_content='%s', update_date='%s', visibility='%s' where id=%s""" % (column_id, title, content, excerpt, commit_content, update_date, visibility, self.id))
		
			#db_conn.commit()
			post_draft = self
		except IntegrityError:
			print 'IntegrityError at post_draft update'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return post_draft
	
	
	@classmethod
	def delete(cls, post_draft_id=None):
		cursor = None

		try:
			cursor = db_conn.gcae('delete from post_draft where id=%s' % (post_draft_id))
			#db_conn.commit()
		except IntegrityError:
			print 'IntegrityError at post_draft delete'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return post_draft_id
	
	
	@classmethod
	def DeleteByPost(cls, post_id=None):
		cursor = None

		try:
			cursor = db_conn.gcae('delete from post_draft where post_id=%s' % (post_id))
			#db_conn.commit()
		except IntegrityError:
			print 'IntegrityError at post_draft DeleteByPost'
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


