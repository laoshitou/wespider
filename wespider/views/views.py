#-*- coding:utf-8 -*-

import sys
import time


from flask import render_template
from flask import request
from flask import jsonify
from flask import session, redirect, url_for, flash, g

from pyquery import PyQuery as pq
import requests

from wespider import app
from wespider.model.user import User
from wespider.model.page_box import PageBox
from wespider.model.source_page import SourcePage
from wespider.model.page import Page
from wespider.model.post_draft import PostDraft
from wespider.model.post_commit import PostCommit
from wespider.model.post import Post
from wespider.util import randbytes
from wespider import config
from .util import require_login

@app.route('/', methods=['GET', 'POST'])
def index():
	user_name = u'未登录' if g.user is None else g.user.user_name
	
	pbs = []
	pages = []

	data_url = "/"
	
	iam_him = True


	if request.method == 'POST':
		start = int(request.form['start'])
		
		if g.user and start != -1:
			pages = Page.getByUser(user_id=g.user.id, start=start, limit=config.PAGESIZE)
			if pages:
				start = start + config.PAGESIZE
				content = render_template('my_page_list.html', pages=pages, iam_him=iam_him)
				return jsonify(success=True, start=start, content=content)
			else:
				start = -1

		return jsonify(success=False, start=start)

	if g.user:
		pbs = PageBox.getByUser(g.user.id)
		pages = Page.getByUser(user_id=g.user.id, start=0, limit=config.PAGESIZE)
		return render_template('boxes.html', user_name=user_name, pbs=pbs, pages=pages, data_url=data_url, start=config.PAGESIZE, iam_him=iam_him)

	return render_template('index.html', user_name=user_name, pbs=pbs, pages=pages)

@app.route('/mybox')
def mybox():
	user_name = u'未登录' if g.user is None else g.user.user_name
	
	pbs = []
	pages = []

	data_url = "/"
	
	iam_him = True


	if request.method == 'POST':
		start = int(request.form['start'])
		
		if g.user and start != -1:
			pages = Page.getByUser(user_id=g.user.id, start=start, limit=config.PAGESIZE)


			if pages:
				start = start + config.PAGESIZE
				content = render_template('my_page_list.html', pages=pages, iam_him=iam_him)
				return jsonify(success=True, start=start, content=content)
			else:
				start = -1

		return jsonify(success=False, start=start)

	if g.user:
		pbs = PageBox.getByUser(g.user.id)

		for pb in pbs:
			pages = Page.getByPagebox(pb_id=pb.id, start=0, limit=5)
			pb.pages = pages
		
		return render_template('lists.html', user_name=user_name, pbs=pbs, pages=pages, data_url=data_url, start=config.PAGESIZE, iam_him=iam_him)

	return render_template('index.html', user_name=user_name, pbs=pbs, pages=pages)



@app.route('/write')
@require_login(msg=u"需要注册并登录后，才能书写或更新文章", flash_sign=True, title=u"WeSpider文章")
def write():
	return render_template('write.html')


@app.route('/user/ajaxLogin', methods=['POST'])
def ajaxLogin():
	
	user_email_name = request.form['user_email_name']
	password = request.form['password']
	
	# 检查用户名/邮箱、密码是不是都填写了
	if not user_email_name or not password:
		return jsonify(success=False)

	user = None
	user = User.verify(user_email_name, password)

	if user is None:
		return jsonify(success=False)
	else:		
		session['session_id'] = user.session_id if user.session_id is not None else randbytes(str(user.id), 16)
		user.update_session(session['session_id'])
		flash(u'登陆成功', 'error')
		return jsonify(success=True)


@app.route('/user/ajaxLogout', methods=['POST'])
def logout():
	if g.user:
		g.user.clear_session()
	
	flash(u'已登出', 'error')
	return jsonify(success=True)


@app.route('/user/ajaxRegister', methods=['POST'])
def ajaxRegister():
	user_name = request.form['user_name']
	user_email = request.form['user_email']
	password = request.form['password']

	# 检查用户名、邮箱、密码是不是都填写了
	if not user_name:
		content = u'请输入用户名'
		return jsonify(success=False, user_name=True, content=content)

	
	if not user_email:
		content = u'请填写正确的邮箱地址'
		return jsonify(success=False, user_email=True, content=content)

	if not password:
		content = u'请输入密码'
		return jsonify(success=False, password=True, content=content)


	# 检查用户名或者邮箱是否已经被注册使用了
	user = None
	
	user = User.getByName(user_name)
	if user:
		content = u'用户名已经被使用'
		return jsonify(success=False, user_name=True, content=content)

	user = User.getByEmail(user_email)
	if user:
		content = u'邮箱已经被使用'
		return jsonify(success=False, user_email=True, content=content)

		
	user = User.getByEmail(user_email)

	user = User.add(user_name, password, user_email)
	
	flash(u'注册成功', 'error')
	return jsonify(success=True, user_id=user.id)



@app.route('/ajaxFetchUrl', methods=['POST'])
def ajaxFetchUrl():
	
	url = request.form['url']
	r = requests.get(url)
	d = pq(r.text)
	add_url_title = d('title').text()
	return jsonify(success=True, add_url_title=add_url_title)



@app.route('/markapage')
def markapage():
	page_url = request.args.get('url', '')
	page_title = request.args.get('title', '')
	page_cnt = request.args.get('clipcnt', '')
	
	pbs = []
	pb_id = ""

	if g.user:
		pbs = PageBox.getByUser(g.user.id)
		pb_id = pbs[0].id

	return render_template('markapage.html', page_url=page_url, page_title=page_title, page_cnt=page_cnt, pbs=pbs, pb_id=pb_id)


@app.route('/clipapage')
def clipapage():
	clip_page_url = request.args.get('url', '')
	clip_page_title = request.args.get('title', '')
	clip_page_cnt = request.args.get('clipcnt', '')
	
	
	return render_template('clipapage.html', clip_page_url=clip_page_url, clip_page_title=clip_page_title, clip_page_cnt=clip_page_cnt)



@app.route('/page/ajaxCreateBox', methods=['POST'])
@require_login(msg=u"需要登录后，才能创建Page Box")
def ajaxCreatePageBox():
	box_name = request.form['box_name']
	box_desc = request.form['box_desc']
	fast = request.form['fast']
	
	# 检查 page box name是否为空
	if not box_name:
		content = u'请输入Page Box 名称'
		if fast == "1":
			flash(content, 'error')
		return jsonify(success=False, box_name=True, content=content)

	# 检查 当前用户是否已经创建过同名的page box
	page_box = None
	page_box = PageBox.getByNameUser(box_name, g.user.id)
	
	if page_box:
		content = u'Page Box [%s] 已存在' % (box_name)
		
		if fast == "1":
			flash(content, 'error')

		return jsonify(success=False, box_name=True, content=content)

	page_box = PageBox.add(box_name, box_desc, g.user.id)


	flash(u'Page Box <%s> 创建成功' % (box_name), 'error')
	return jsonify(success=True, box_name=box_name)




@app.route('/page/ajaxEditBox', methods=['POST'])
@require_login(msg=u"需要登录后，才能编辑Page Box")
def ajaxEditPageBox():
	box_name = request.form['box_name']
	box_desc = request.form['box_desc']
	pb_id = request.form['pb_id']
	
	# 检查 page box name是否为空
	if not box_name:
		content = u'请输入Page Box 名称'
		return jsonify(success=False, box_name=True, content=content)

	# 检查 当前用户是否已经创建过同名的page box
	page_box = None
	page_box = PageBox.getByNameUser(box_name, g.user.id)
	
	if page_box and page_box.id != int(pb_id):
		content = u'您已经创建了<%s>的Page Box' % (box_name)
		return jsonify(success=False, box_name=True, content=content)

	if page_box is None:
		page_box = None
		page_box = PageBox.get(pb_id)
	
	if page_box.user_id != g.user.id:
		content = u'您没有编辑<%s>Page Box的权限' % (box_name)
		return jsonify(success=False, box_name=True, content=content)

	page_box = page_box.update(box_name, box_desc)


	flash(u'Page Box <%s> 更新成功' % (box_name), 'error')
	return jsonify(success=True, box_name=box_name)


@app.route('/page/ajaxDelPageBox', methods=['POST'])
@require_login(msg=u"需要登录后，才能删除Page Box")
def ajaxDelPageBox():
	box_name = request.form['box_name']
	pb_id = request.form['pb_id']
	
	pages = None	
	page_box = None
	page_box = PageBox.get(pb_id)

	if page_box is None:
		content = u'您要删除的<%s>Page Box不存在' % (box_name)
		return jsonify(success=False, content=content, box_name=True)
	
	if page_box.user_id != g.user.id:
		content = u'您没有删除<%s>Page Box的权限' % (box_name)
		return jsonify(success=False, content=content, box_name=True)
	
	pages = Page.getByPagebox(pb_id)

	if pages:
		content = u'您要删除的<%s>Page Box下还有收藏的Page，无法删除' % (box_name)
		return jsonify(success=False, content=content, box_name=True)

	PageBox.delete(pb_id)
	flash(u'Page Box <%s> 删除成功' % (box_name), 'error')
	return jsonify(success=True)



@app.route('/page/ajaxMoveToBox', methods=['POST'])
@require_login(msg=u"需要登录后，才能移动Page")
def ajaxMoveToBox():
	page_id = request.form['page_id']
	pb_id = request.form['pb_id']
	
	page = None	
	page_box = None

	page_box = PageBox.get(pb_id)
	page = Page.get(page_id)

	if page_box is None:
		flash(u'您要移向的Page Box不存在', 'error')
		return jsonify(success=False)
	
	if page is None:
		flash(u'您要移动的Page不存在', 'error')
		return jsonify(success=False)

	if page_box.user_id != g.user.id:
		flash(u'您没有移动到<%s>Page Box的权限' % (page_box.name), 'error')
		return jsonify(success=False)
	
	if page.user_id != g.user.id:
		flash(u'您没有移动<%s>Page Box的权限' % (page.title), 'error')
		return jsonify(success=False)

	

	page.update(page_box_id=pb_id)

	flash(u'Page<%s> 成功移动到 Page Box<%s>' % (page.title, page_box.name), 'error')
	return jsonify(success=True)


@app.route('/page/ajaxEdit', methods=['POST'])
@require_login(msg=u"需要登录后，才能编辑Page")
def ajaxEditPage():
	page_id = request.form['page_id']
	page_tip = request.form['page_tip']
	page_title = request.form['page_title']
	
	page = None	

	page = Page.get(page_id)

	
	if page is None:
		flash(u'您要编辑的Page不存在', 'error')
		return jsonify(success=False)

	
	if page.user_id != g.user.id:
		flash(u'您没有编辑<%s>Page的权限' % (page.title), 'error')
		return jsonify(success=False)

	

	page.update(page_title=page_title, page_tip=page_tip)

	flash(u'Page<%s> 编辑成功' % (page.title), 'error')
	return jsonify(success=True)



@app.route('/page/ajaxDel', methods=['POST'])
@require_login(msg=u"需要登录后，才能取消收藏Page")
def ajaxDelPage():
	page_id = request.form['page_id']
	
	page = None	

	page = Page.get(page_id)

		
	if page is None:
		flash(u'您要取消收藏的Page不存在', 'error')
		return jsonify(success=False)
	
	if page.user_id != g.user.id:
		flash(u'您没有取消收藏<%s>的权限' % (page.title), 'error')
		return jsonify(success=False)
	

	Page.delete(page_id)

	flash(u'Page<%s> 已经被成功取消收藏' % (page.title), 'error')
	return jsonify(success=True)



@app.route('/page/ajaxSearch', methods=['POST'])
@require_login(msg=u"需要登录后，才能搜索Page")
def ajaxSearchPage():
	pb_id = request.form['pb_id']
	pg_skw = request.form['pg_skw']
	start = int(request.form['start'])
	
	pages = None
	page_box = None
	data_url = '/page/ajaxSearch'

	if not pg_skw:
		flash(u'请输入搜索关键词', 'error')
		return jsonify(success=False)


	if pb_id:
		page_box = PageBox.get(pb_id)


	pages = Page.search(pg_skw=pg_skw, pb_id=pb_id, user_id=g.user.id, start=start, limit=config.PAGESIZE)
	
	if pages:
		start = start + config.PAGESIZE
		content = render_template('my_page_list.html', pages=pages)
		return jsonify(success=True, content=content, data_url=data_url, pg_skw=pg_skw, start=start)
	else:
		start = -1
		return jsonify(success=True, content="", data_url=data_url, pg_skw=pg_skw, start=start)



@app.route('/page/ajaxMarkSubmit', methods=['POST'])
@require_login(msg=u"需要登录后，才能收藏Page")
def ajaxMarkSubmit():
	pb_id = request.form['pb_id']
	page_url = request.form['page_url']
	o_page_title = request.form['o_page_title']
	page_title = request.form['page_title']
	page_tip = request.form['page_tip'] or ""

	page_title = page_title or o_page_title

	source_page = SourcePage.getByUrl(page_url)

	if source_page is None:
		source_page = SourcePage.add(o_page_title, page_url)
	
	page = Page.getByUrl(page_title, page_url, g.user.id)

	if page:
		flash(u'您已经收藏过', 'error')
		return jsonify(success=False, marked=True, page_id=page.id)
	
	mark_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	page = Page.add(source_page_id=source_page.id, page_box_id=pb_id, user_id=g.user.id, title=page_title, url=page_url, tip=page_tip, date=mark_date)
	
	flash(u'收藏成功', 'error')
	return jsonify(success=True, page_id=page.id)


@app.route('/page/ajaxMarkSubmitCallback')
def ajaxMarkSubmitCallback():
	page_id = request.args.get('page_id', '')

	page = Page.get(page_id)

	return render_template('ajaxmarksubmitcallback.html', page=page)


@app.route('/pagebox/<int:pb_id>', methods=['GET', 'POST'])
def pagebox(pb_id):
	pbs = []
	pages = []
	iam_him = False
		
	data_url = '/pagebox/%s' % (pb_id)
	
	pb = PageBox.get(pb_id)

	if g.user and g.user.id == pb.user_id:
		iam_him = True

	if request.method == 'POST':
		start = int(request.form['start'])
		
		if start != -1:
			pages = Page.getByPagebox(pb_id=pb_id, start=start, limit=config.PAGESIZE)
			
			if pages:
				start = start + config.PAGESIZE
				content = render_template('my_page_list.html', pages=pages, iam_him=iam_him)
				return jsonify(success=True, start=start, content=content)
			else:
				start = -1

		return jsonify(success=False, start=start)
	
	pages = Page.getByPagebox(pb_id=pb_id, start=0, limit=config.PAGESIZE)

	if g.user:
		pbs = PageBox.getByUser(g.user.id, exclude_id=pb_id)
	
	
		
	return render_template('pagebox.html', pbs=pbs, pages=pages, pb=pb, pb_id=pb_id, start=config.PAGESIZE, data_url=data_url, iam_him=iam_him)


@app.route('/post/ajaxSaveDraft', methods=['POST'])
@require_login(msg=u"需要登录后，才能保存草稿")
def ajaxSaveDraft():
	
	post_draft_id = request.form['post_draft_id'] or 0
	post_draft_id = int(post_draft_id)

	post_id = request.form['post_id'] or 0
	post_id = int(post_id)

	post_title = request.form['post_title'] or None
	post_content = request.form['post_content'] or ""
	commit_content = request.form['commit_content'] or ""
	visibility = request.form['visibility'] or 'self'

	update_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
	column_id = 0
	
	if not post_title:
		content = u'请输入标题'
		return jsonify(success=False, content=content)

	if post_draft_id:
		post_draft = PostDraft.get(post_draft_id)
		post_draft.update(column_id=column_id, title=post_title, content=post_content, excerpt=post_content, commit_content=commit_content, update_date=update_date, visibility=visibility)
		flash(u'保存草稿成功', 'error')
	else:
		post_draft = PostDraft.add(post_id=post_id, column_id=column_id, title=post_title, content=post_content, excerpt=post_content, commit_content=commit_content, update_date=update_date, visibility=visibility, user_id=g.user.id)
		flash(u'保存草稿成功', 'error')
		
	return jsonify(success=True, post_draft_id=post_draft.id)


@app.route('/post/ajaxDeleteDraft', methods=['POST'])
@require_login(msg=u"需要登录后，才能删除草稿")
def ajaxDeleteDraft():
	
	post_draft_id = request.form['post_draft_id'] or 0
	post_draft_id = int(post_draft_id)

	if post_draft_id:
		post_draft = PostDraft.get(post_draft_id)
		PostDraft.delete(post_draft.id)
		flash(u'草稿<%s>删除成功' % (post_draft.title), 'error')
		
	return jsonify(success=True)




@app.route('/post/draft/<int:post_draft_id>/edit')
@require_login(msg=u"需要登录后，才能编辑草稿", flash_sign=True, title = u"WeSpider文章")
def DraftEdit(post_draft_id):
	post_draft_id = int(post_draft_id)

	
	post_draft = PostDraft.get(post_draft_id)

	if not post_draft or post_draft.user_id != g.user.id:
		flash(u'要编辑的草稿不存在', 'error')
		title = u"WeSpider文章"
		content = u'要编辑的草稿不存在'
		return render_template('access_denied.html', title=title, content=content)

	
	

	return render_template('post_draft_edit.html', post_draft=post_draft)



@app.route('/post')
def post():
	user_name = u'未登录' if g.user is None else g.user.user_name
	
	pds = []

	data_url = "/post"
	
	iam_him = True


	if request.method == 'POST':
		start = int(request.form['start'])
		
		if g.user and start != -1:
			pages = Page.getByUser(user_id=g.user.id, start=start, limit=config.PAGESIZE)
			if pages:
				start = start + config.PAGESIZE
				content = render_template('my_post_list.html', pages=pages, iam_him=iam_him)
				return jsonify(success=True, start=start, content=content)
			else:
				start = -1

		return jsonify(success=False, start=start)

	if g.user:
		pds = PostDraft.getByUser(user_id=g.user.id, start=0, limit=config.PAGESIZE)
		pts = Post.getByUser(user_id=g.user.id, start=0, limit=config.PAGESIZE)
		return render_template('user_post.html', user_name=user_name, pds=pds, pts=pts, data_url=data_url, start=config.PAGESIZE, iam_him=iam_him)

	return render_template('post.html', user_name=user_name, pds=pds)



@app.route('/post/ajaxCommit', methods=['POST'])
@require_login(msg=u"需要登录后，才能提交文章")
def ajaxPostCommit():
	post_draft_id = request.form['post_draft_id'] or 0
	post_draft_id = int(post_draft_id)

	post_id = request.form['post_id'] or 0
	post_id = int(post_id)

	post_title = request.form['post_title'] or None
	post_content = request.form['post_content'] or ""
	commit_content = request.form['commit_content'] or ""
	visibility = request.form['visibility'] or 'self'

	update_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
	column_id = 0
	
	if not post_title:
		content = u'请输入标题'
		return jsonify(success=False, content=content)
	
	if not commit_content:
		content = u'请输入变更记录'
		return jsonify(success=False, content=content)

	if post_id:
		post = Post.get(post_id)
		post.update(column_id=column_id, title=post_title, content=post_content, excerpt=post_content, commit_content=commit_content, update_date=update_date, visibility=visibility)
	else:
		post = Post.add(column_id=column_id, title=post_title, content=post_content, excerpt=post_content, commit_content=commit_content, update_date=update_date, visibility=visibility, user_id=g.user.id)
	
	post_commit = PostCommit.add(post_id=post.id, column_id=column_id, title=post_title, content=post_content, excerpt=post_content, commit_content=commit_content, update_date=update_date, visibility=visibility, user_id=g.user.id)

	if post_draft_id:
		PostDraft.delete(post_draft_id)
		
	flash(u'文章提交成功', 'error')
	return jsonify(success=True, post_id=post.id)






@app.route('/post/<int:post_id>/edit')
@require_login(msg=u"需要注册并登录后，才能书写或更新文章", flash_sign=True, title=u"WeSpider文章更新")
def post_single_edit(post_id):
	post_id = int(post_id)
	
	post_draft = PostDraft.getByPost(post_id)
	
	if post_draft:
		return redirect("/post/draft/%s/edit" % (post_draft.id))

	post = Post.get(post_id)
	
	if post.user_id != g.user.id:
		title = u"WeSpider文章更新"
		content = u'没有更新文章《%s》的权限' % (post.title)
		return render_template('access_denied.html', title=title, content=content)
	
	return render_template('post_single_edit.html', post=post)


@app.route('/post/<int:post_id>')
def post_single(post_id):
	post_id = int(post_id)
	
	
	post = Post.get(post_id)
	
	if post is None or (post.visibility=="self" and (not g.user or g.user.id != post.user_id)):
		title = u"WeSpider文章"
		content = u'文章不存在，或者被作者设为私密文章'
		return render_template('access_denied.html', title=title, content=content)

	author = User.get(post.user_id)
	pcs = PostCommit.getByPost(post.id)
	visibility = u"私密" if post.visibility == "self" else u"公开"
	
	return render_template('post_single.html', post=post, pcs=pcs, author=author, visibility=visibility)


@app.route('/post/ajaxDelete', methods=['POST'])
@require_login(msg=u"需要登录后，才能删除文章")
def ajaxDeletePost():
	
	post_id = request.form['post_id'] or 0
	post_id = int(post_id)

	if post_id:
		post = Post.get(post_id)
		PostDraft.DeleteByPost(post.id)
		PostCommit.DeleteByPost(post.id)
		Post.Delete(post_id)
		flash(u'文章<%s>删除成功' % (post.title), 'error')
		
	return jsonify(success=True)


