$(function() {

	/*
	$('textarea.autosize').on('focus', function(){
		$(this).autosize();
	});
	*/

	//编辑器初始化
	/*
	if (typeof (myMarkdownSettings) != 'undefined' && $('.advanced_editor')) {
		$('.advanced_editor').markItUp(myMarkdownSettings);

		$.setEditorPreview();
	} else if ($('.markItUpPreviewFrame')) {
		$('.markItUpPreviewFrame').hide();
	}
	*/

	//当编辑框快要到达底部的时候，自动向上滚动
	/*
	$('#write-post-wrap').resize(function () {
		var win_h = $(window).height();
		var win_st = $(window).scrollTop();
		var wpw_h = $('#write-post-wrap').height(); 
		var wpw_st = $('#write-post-wrap').scrollTop(); 
		var content = 'win_h: '+win_h+', win_st: '+win_st+', wpw_h: '+wpw_h+', wpw_st: '+wpw_st;
		$('#test_output').html(content);

		if((wpw_h + 200)>(win_h+win_st)) {
			$('html,body').animate({scrollTop: (win_st+500)+'px'}, 800);
		}
	});
	*/
	
	
	

	$(document).on("click", '#reg-submit-btn', function(e) {
		if($(this).attr('id') =="reg-submit-btn" || e.keyCode==13) {
			var user_name = $('#regform input#user_name').val();
			var user_email = $('#regform input#user_email').val();
			var password = $('#regform input#password').val();

			$('.reg-form-wrap .alert').hide();

			
			
			$.ajax({
				type: "post",
				url: "/user/ajaxRegister",
				dataType: 'json',
				data: {
					'user_name': user_name,
					'user_email': user_email,
					'password': password
				},
				success: function(ret_data) {
					if(ret_data.success) {
						location.href = "/";
					} else {
						if (ret_data.user_name) {
							$('#regform #reg_user_name_warn .ztag').html(ret_data.content);
							$('#regform #reg_user_name_warn').show();
						}

						if (ret_data.user_email) {
							$('#regform #reg_user_email_warn .ztag').html(ret_data.content);
							$('#regform #reg_user_email_warn').show();
						}

						if (ret_data.password) {
							$('#regform #reg_password_warn .ztag').html(ret_data.content);
							$('#regform #reg_password_warn').show();
						}

					}

				}
			});
		}
	});
	
	

	$(document).on("click", '#logout-submit-btn', function(e) {
		$.ajax({
			type: "post",
			url: "/user/ajaxLogout",
			dataType: 'json',
			success: function(ret_data) {
				location.href = window.location.href;
			}
		});
	});
	
	
	$(document).on("click", '#login-submit-btn', function(e) {
		if($(this).attr('id') =="login-submit-btn" || e.keyCode==13) {
			var user_email_name = $('#loginform input#user_email_name').val();
			var password = $('#loginform input#password').val();

			$('.login-form-wrap .alert').hide();

			$.ajax({
				type: "post",
				url: "/user/ajaxLogin",
				dataType: 'json',
				data: {
					'user_email_name': user_email_name,
					"password": password
				},
				success: function(ret_data) {
					if (ret_data.success) {
						location.href = window.location.href;
					} else {
						$('#loginform #loginwarn').show();
					}
				}
			});
		}
	});

	$(document).on("keydown", '.login-form-wrap input', function(e) {
		if(e.keyCode==13) {	
			$('#login-submit-btn').click();
		}
	});
	
	$(document).on("keydown", '.reg-form-wrap input', function(e) {
		if(e.keyCode==13) {	
			$('#reg-submit-btn').click();
		}
	});

	$('#LoginModal').on('hide.bs.modal', function (e) {
		$('.login-form-wrap .alert').hide();	
	});


	$('#RegModal').on('hide.bs.modal', function (e) {
		$('.reg-form-wrap .alert').hide();	
	});
	
	
	
	$(document).on("click", "#SaveAsDraftBtn", function(e) {
		var post_id = $(this).attr('post_id');
		var post_draft_id = $(this).attr('post_draft_id');
		var post_title = $('#PostTitle').val();
		var post_content = $('#advanced_editor').val();
		var commit_content = $('#commit_editor').val();
		var visibility = $('input:radio[name="VisibilityOption"]:checked').val();
		var submit_url = $(this).attr('submit_url');



		$.ajax({
			type: "post",
			url: submit_url,
			dataType: 'json',
			data: {
				'post_title': post_title,
				'post_content': post_content,
				'commit_content': commit_content,
				'post_id': post_id,
				'post_draft_id': post_draft_id,
				'visibility': visibility
			},
			success: function(ret_data) {
				if (ret_data.success) {
					var newHref = "/post/draft/"+ret_data.post_draft_id+"/edit";
					location.href = newHref;	
				} else {
				}
			}
		});

	});
	
	
	
	$(document).on("click", "#CommitBtn", function(e) {
		var post_id = $(this).attr('post_id');
		var post_draft_id = $(this).attr('post_draft_id');
		var post_title = $('#PostTitle').val();
		var post_content = $('#advanced_editor').val();
		var commit_content = $('#commit_editor').val();
		var visibility = $('input:radio[name="VisibilityOption"]:checked').val();
		var submit_url = $(this).attr('submit_url');


		$.ajax({
			type: "post",
			url: submit_url,
			dataType: 'json',
			data: {
				'post_title': post_title,
				'post_content': post_content,
				'commit_content': commit_content,
				'post_id': post_id,
				'post_draft_id': post_draft_id,
				'visibility': visibility
			},
			success: function(ret_data) {
				if (ret_data.success) {
					var newHref = "/post/"+ret_data.post_id;
					location.href = newHref;	
				} else {
				}
			}
		});

	});

	
	$(document).on("click", '#open_install_add_btn', function(e) {
		$('#install_add_btn_wrap').toggle();
	});
	
	
	$(document).on("click", '#add_url_cancel_btn', function(e) {
		window.close();
		return true;
	});
	
	$('#my_post_tab a').click(function (e) {
		e.preventDefault()
		$(this).tab('show')
	});
	
	
	$(document).on("click", '#create_page_box_submit_btn', function(e) {
		var create_page_box_name = $('input#create_page_box_name').val();
		var create_page_box_desc = $('textarea#create_page_box_desc').val();
		
		$('#create_my_page_box .alert').hide();
		
		$.ajax({
			type: "post",
			url: "/page/ajaxCreateBox",
			dataType: 'json',
			data: {
				'box_name': create_page_box_name,
				'box_desc': create_page_box_desc,
				'fast':0
			},
			success: function(ret_data) {
				if (ret_data.success) {
					location.href = "/";
				} else {
					if (ret_data.box_name) {
						$('#box_name_warn .ztag').html(ret_data.content);
						$('#box_name_warn').show();
					}
					
					if (ret_data.nologin) {
						$('#box_name_warn .ztag').html(ret_data.tip);
						$('#box_name_warn').show();
					}

				}
			}
		});
	});
	
	
	$(document).on("click", '#fast_create_page_box_btn', function(e) {
		var create_page_box_name = $('input#fast_page_box_name').val();
		var create_page_box_desc = "";
		
		
		$.ajax({
			type: "post",
			url: "/page/ajaxCreateBox",
			dataType: 'json',
			data: {
				'box_name': create_page_box_name,
				'box_desc': create_page_box_desc,
				'fast': 1
			},
			success: function(ret_data) {
				location.href = window.location.href;
			}
		});
	});

	
	$(document).on("click", '#edit_page_box_submit_btn', function(e) {
		var edit_page_box_name = $('input#edit_page_box_name').val();
		var edit_page_box_desc = $('textarea#edit_page_box_desc').val();
		var pb_id = $(this).attr('pb_id');
		
		$('#edit_my_page_box .alert').hide();
		
		$.ajax({
			type: "post",
			url: "/page/ajaxEditBox",
			dataType: 'json',
			data: {
				'pb_id': pb_id,
				'box_name': edit_page_box_name,
				'box_desc': edit_page_box_desc
			},
			success: function(ret_data) {
				if (ret_data.success) {
					location.href = window.location.href;
				} else {
					if (ret_data.box_name) {
						$('#edit_box_name_warn .ztag').html(ret_data.content);
						$('#edit_box_name_warn').show();
					}
					
					if (ret_data.nologin) {
						$('#box_name_warn .ztag').html(ret_data.tip);
						$('#box_name_warn').show();
					}

				}
			}
		});
	});
	
	
	$(document).on("click", '#del_page_box_submit_btn', function(e) {
		var pb_id = $(this).attr('pb_id');
		var box_name = $(this).attr('box_name');
			
		$('#del_my_page_box .alert').hide();
		
		$.ajax({
			type: "post",
			url: "/page/ajaxDelPageBox",
			dataType: 'json',
			data: {
				'pb_id': pb_id,
				'box_name': box_name
			},
			success: function(ret_data) {
				if (ret_data.success) {
					location.href = "/";
				} else {
					if (ret_data.box_name) {
						$('#del_box_name_warn .ztag').html(ret_data.content);
						$('#del_box_name_warn').show();
					}
					
					if (ret_data.nologin) {
						$('#del_box_name_warn .ztag').html(ret_data.tip);
						$('#del_box_name_warn').show();
					}

				}
			}
		});
	});

	
	$(document).on("click", '#select_clip_box_list ul li', function(e) {
		$('#select_clip_box_list ul li').removeClass('selected');
		$(this).addClass('selected');
		pb_id = $(this).attr('pb_id');
		$('.select_pb_value_holder').attr('pb_id', pb_id);
	});
	
	$(document).on("click", '#add_url_confirm_btn', function(e) {
		pb_id = $(this).attr('pb_id');
		page_url = $('#add_url_url input').val();
		o_page_title = $('#o_page_title input').val();
		page_title = $('#add_url_title input').val();
		page_tip = $('#add_url_desc textarea').val();

		
		$.ajax({
			type: "post",
			url: "/page/ajaxMarkSubmit",
			dataType: 'json',
			data: {
				'pb_id': pb_id,
				'page_url': page_url,
				'o_page_title': o_page_title,
				'page_title': page_title,
				'page_tip': page_tip
			},
			success: function(ret_data) {
				if (ret_data.success) {
					location.href="/page/ajaxMarkSubmitCallback?page_id="+ret_data.page_id;
				} else {
					location.href=window.location.href;					
				}
			}
		});

	});
	
	
	$(document).on("click", '.page_move_btn', function(e) {
		var page_id = $(this).attr('page_id');
		var page_title = $(this).attr('page_title');
		
		$('#TargetPageBoxModal #moved_page_title').html(page_title);
		$('#TargetPageBoxModal #moveto_page_box_submit_btn').attr('page_id', page_id);

		$('#TargetPageBoxModal').modal();

	});
	
	
	$(document).on("click", '#moveto_page_box_submit_btn', function(e) {
		pb_id = $(this).attr('pb_id');
		page_id = $(this).attr('page_id');
		
		$.ajax({
			type: "post",
			url: "/page/ajaxMoveToBox",
			dataType: 'json',
			data: {
				'pb_id': pb_id,
				'page_id': page_id
			},
			success: function(ret_data) {
				location.href=window.location.href;					
			}
		});

	});
	
	
	$(document).on("click", '.page_edit_btn', function(e) {
		var page_id = $(this).attr('page_id');
		var page_url = $(this).attr('page_url');
		var page_title = $(this).attr('page_title');
		var page_tip = $('#page_tip_wrap_'+page_id).html();
		
		$('#EditPageModal #add_url_url input').val(page_url);
		$('#EditPageModal #add_url_title input').val(page_title);
		$('#EditPageModal #add_url_desc textarea').val(page_tip);
		$('#EditPageModal #edit_page_submit_btn').attr('page_id', page_id);

		$('#EditPageModal').modal();

	});

	
	$(document).on("click", '.page_del_btn', function(e) {
		var page_id = $(this).attr('page_id');
		var page_title = $(this).attr('page_title');
		
		$('#DelPageModal #del_page_title').html(page_title);
		$('#DelPageModal #del_page_submit_btn').attr('page_id', page_id);

		$('#DelPageModal').modal();

	});
	
	
	$(document).on("click", '#edit_page_submit_btn', function(e) {
		page_id = $(this).attr('page_id');
		page_title = $('#EditPageModal #add_url_title input').val();
		page_tip = $('#EditPageModal #add_url_desc textarea').val();
		
		$.ajax({
			type: "post",
			url: "/page/ajaxEdit",
			dataType: 'json',
			data: {
				'page_id': page_id,
				'page_title': page_title,
				'page_tip': page_tip
			},
			success: function(ret_data) {
				location.href=window.location.href;
			}
		});

	});

	
	$(document).on("click", '#del_page_submit_btn', function(e) {
		page_id = $(this).attr('page_id');
		
		$.ajax({
			type: "post",
			url: "/page/ajaxDel",
			dataType: 'json',
			data: {
				'page_id': page_id
			},
			success: function(ret_data) {
				location.href=window.location.href;
			}
		});

	});
	
	
	$(document).on("click", '#pg_skw_btn', function(e) {
		var pb_id = $(this).attr('pb_id');
		var start = $(this).attr('start');
		var pg_skw = $('input#pg_skw').val();
		
		
		$.ajax({
			type: "post",
			url: "/page/ajaxSearch",
			dataType: 'json',
			data: {
				'pg_skw': pg_skw,
				'start': start,
				'pb_id': pb_id
			},
			success: function(ret_data) {
				if(ret_data.success) {
					$('#search_my_page_ret_summary h2 span.page_search_keyword').html(pg_skw);
					$('#search_my_page_ret_summary').show();
					$('#my_page_list_wrap ul').html(ret_data.content);
					$('.loadmorepage button').attr('data_url', ret_data.data_url);
					$('.loadmorepage button').attr('pg_skw', ret_data.pg_skw);
					$('.loadmorepage button').attr('start', ret_data.start);

					

				} else {
					location.href=window.location.href;
				}
			}
		});

	});
	
	
	$(document).on("click", '.loadmorepage button', function(e) {
		var pb_id = $(this).attr('pb_id');
		var data_url = $(this).attr('data_url');
		var start = $(this).attr('start');
		var pg_skw = $(this).attr('pg_skw');
		
		
		$.ajax({
			type: "post",
			url: data_url,
			dataType: 'json',
			data: {
				'pg_skw': pg_skw,
				'start': start,
				'pb_id': pb_id
			},
			success: function(ret_data) {
				if(ret_data.success) {
					$('.loadmorepage button').attr('start', ret_data.start);
					$('#my_page_list_wrap ul').append(ret_data.content);
					
					
				} else {
					$('.loadmorepage button').attr('start', ret_data.start);
					
					if(ret_data.start == -1) {
						$('.loadmorepage').fadeOut();	
					}
				}
			}
		});

	});
	
	
	$(document).on("click", '.draft_del_btn', function(e) {
		var post_draft_id = $(this).attr('post_draft_id');
		var post_draft_title = $(this).attr('post_draft_title');
		
		$('#DelDraftModal #del_draft_title').html(post_draft_title);
		$('#DelDraftModal #del_draft_submit_btn').attr('post_draft_id', post_draft_id);

		$('#DelDraftModal').modal();

	});
	
	$(document).on("click", '#del_draft_submit_btn', function(e) {
		post_draft_id = $(this).attr('post_draft_id');
		
		$.ajax({
			type: "post",
			url: "/post/ajaxDeleteDraft",
			dataType: 'json',
			data: {
				'post_draft_id': post_draft_id
			},
			success: function(ret_data) {
				location.href=window.location.href;
			}
		});

	});
	
	
	$(document).on("click", '.post_del_btn', function(e) {
		var post_id = $(this).attr('post_id');
		var post_title = $(this).attr('post_title');
		
		$('#DelPostModal #del_post_title').html(post_title);
		$('#DelPostModal #del_post_submit_btn').attr('post_id', post_id);

		$('#DelPostModal').modal();

	});
	
	$(document).on("click", '#del_post_submit_btn', function(e) {
		post_id = $(this).attr('post_id');
		
		$.ajax({
			type: "post",
			url: "/post/ajaxDelete",
			dataType: 'json',
			data: {
				'post_id': post_id
			},
			success: function(ret_data) {
				location.href=window.location.href;
			}
		});

	});

	
});
