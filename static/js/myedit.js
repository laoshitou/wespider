(function() {
	$(function() {
		var editor;
		return editor = new Simditor({
			textarea: $('#advanced_editor'),
			placeholder: '这里输入文字...',
			pasteImage: true,
			toolbar: ['title', 'bold', 'italic', 'underline', 'strikethrough', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'image', 'hr'],
			defaultImage: 'assets/images/image.png',
			upload: location.search === '?upload' ? {
				url: '/upload'
			} : false
		});
	});

}).call(this);



