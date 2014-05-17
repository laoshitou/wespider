// nodejs server for upload testing

var express = require('express');
var path = require('path')
var fs = require('fs');
var app = express();

app.use(express.bodyParser({uploadDir:'./_site/assets/images'}));

app.post('/upload', function(req, res) {
	var tmp_path = req.files.upload_file.path;
	var target_path = path.resolve('_site/assets/images', req.files.upload_file.name);
	fs.rename(tmp_path, target_path, function(err) {
		if (err) throw err;
		fs.unlink(tmp_path, function() {
			if (err) throw err;
			res.send({ file_path: 'assets/images/' + req.files.upload_file.name });
		});
	});
});

module.exports = app;
