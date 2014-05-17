#-*- coding:utf-8 -*-

from MySQLdb import IntegrityError

from wespider.store import db_conn
from wespider import config

class PageBox(object):

	def __init__(self):
		self.id = None
		self.user_id = None
		self.name = None
		self.content = None
	
	def __repr__(self):
		return "<PageBox id=%s, name=%s>" % (self.id, self.name)

	__str__ = __repr__
	
	
	
	@classmethod
    	def get(cls, id):
		
		cursor = db_conn.gcae('select id, name, content, user_id from page_box where id=%s' % (id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			pb = cls()
			pb.id = row[0]
			pb.name = row[1]
			pb.content = row[2]
			pb.user_id = row[3]
			return pb
		
		return None	
	
	
	@classmethod
    	def getByNameUser(cls, box_name, user_id):
		
		cursor = db_conn.gcae('select id, name, content, user_id from page_box where name="%s" and user_id=%s' % (box_name, user_id))
		
		row = cursor.fetchone()
	        cursor and cursor.close()
		
		if row:
			pb = cls()
			pb.id = row[0]
			pb.name = row[1]
			pb.content = row[2]
			pb.user_id = row[3]
			return pb
		
		return None	
	
	
	@classmethod
    	def getByUser(cls, user_id, exclude_id=None):
		
		if exclude_id is None:
			cursor = db_conn.gcae('select id, name, content, user_id from page_box where user_id=%s' % (user_id))
		else:
			cursor = db_conn.gcae('select id, name, content, user_id from page_box where user_id=%s and id <> %s' % (user_id, exclude_id))
		
		data = cursor.fetchall()
	        cursor and cursor.close()
		
		pbs = []

		if data:
			for row in data:
				pb = cls()
				pb.id = row[0]
				pb.name = row[1]
				pb.content = row[2]
				pb.user_id = row[3]
				pbs.append(pb)
		
		return pbs


	@classmethod
	def add(cls, name=None, content=None, user_id=None):
		cursor = None
		page_box = None

		name = "" if name is None else name
		content = "" if content is None else content
		user_id = "" if user_id is None else user_id
		
		try:
			cursor = db_conn.gcae("""insert into page_box (name, content, user_id) 
						    values (%s, %s, %s)""", (name, content, user_id))
		
			pb_id = cursor.lastrowid
			#db_conn.commit()
			page_box = cls.get(pb_id)
		except IntegrityError:
			print 'IntegrityError at page box add'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return page_box


	def update(self, name=None, content=None):
		cursor = None
		page_box = None

		name = "" if name is None else name
		content = "" if content is None else content
		
		try:
			cursor = db_conn.gcae('update page_box set name="%s", content="%s" where id=%s' % (name, content, self.id))
		
			#db_conn.commit()
			page_box = self
		except IntegrityError:
			print 'IntegrityError at page box update'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return page_box

	@classmethod
	def delete(cls, pb_id=None):
		cursor = None

		try:
			cursor = db_conn.gcae('delete from page_box where id=%s' % (pb_id))
			#db_conn.commit()
		except IntegrityError:
			print 'IntegrityError at page box delete'
			#db_conn.rollback()
		finally:
			cursor and cursor.close()

		return pb_id

