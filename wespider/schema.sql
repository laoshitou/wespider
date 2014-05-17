-- ----------------------------
-- create user table
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`user_name` varchar(255),
	`user_email` varchar(1024),
	`real_name` varchar(255),
	`password` char(32),
	`phone` varchar(255),
	`status` varchar(20),
	`session_id` varchar(20),
	`avatar_big_url` text,
	`avatar_mid_url` text,
	`avatar_small_url` text,
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1000000 DEFAULT CHARSET=utf8;


-- ----------------------------
-- create column table
-- ----------------------------
DROP TABLE IF EXISTS `column`;
CREATE TABLE `column` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`title` text, -- 专栏名称
	`content` longtext, -- 专栏介绍
	`excerpt` text, -- 专栏介绍摘要
	`author_id` bigint(20) unsigned DEFAULT '0',
	`update_date` datetime DEFAULT '0000-00-00 00:00:00',
	`visibility` varchar(20) NOT NULL DEFAULT 'public',-- 可见性(public公开/private私藏)
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;


-- ----------------------------
-- create post table
-- ----------------------------
DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`column_id` bigint(20) unsigned, -- 所属专栏ID
	`title` text, -- 最新的post_commit的title 
	`content` longtext, -- 最新的post_commit的content
	`excerpt` text, -- 最新的post_commit的excerpt
	`commit_content` text, -- 最新提交的备注
	`author_id` bigint(20) unsigned DEFAULT '0',
	`update_date` datetime DEFAULT '0000-00-00 00:00:00',
	`visibility` varchar(20) NOT NULL DEFAULT 'public',-- 可见性(public公开/private私藏)
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;


-- ----------------------------
-- create post_commit table(对post每一次修改提交的版本记录)
-- ----------------------------
DROP TABLE IF EXISTS `post_commit`;
CREATE TABLE `post_commit` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`post_id` bigint(20) unsigned, -- 外键: post的主ID
	`column_id` bigint(20) unsigned, -- 所属专栏ID
	`title` text,
	`content` longtext,
	`excerpt` text,
	`commit_content` text, -- 本次提交的备注
	`author_id` bigint(20) unsigned DEFAULT '0',
	`update_date` datetime DEFAULT '0000-00-00 00:00:00',
	`visibility` varchar(20) NOT NULL DEFAULT 'public',-- 可见性(public公开/private私藏)
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;


-- ----------------------------
-- create post_draft table(对post每次修改，先生成草稿，待提交后，生成新的commit与更新Post)
-- ----------------------------
DROP TABLE IF EXISTS `post_draft`;
CREATE TABLE `post_draft` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`post_id` bigint(20) unsigned, -- 外键: post的主ID
	`column_id` bigint(20) unsigned, -- 所属专栏ID
	`title` text,
	`content` longtext,
	`excerpt` text,
	`commit_content` text, -- 本次保存的备注
	`author_id` bigint(20) unsigned DEFAULT '0',
	`update_date` datetime DEFAULT '0000-00-00 00:00:00',
	`visibility` varchar(20) NOT NULL DEFAULT 'public',-- 可见性(public公开/private私藏)
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;




-- ----------------------------
-- create source_page table
-- ----------------------------
DROP TABLE IF EXISTS `source_page`;
CREATE TABLE `source_page` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`title` text, -- source_page标题
	`url` text, -- source_page url
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;



-- ----------------------------
-- create page table
-- ----------------------------
DROP TABLE IF EXISTS `page`;
CREATE TABLE `page` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`source_page_id` bigint(20) unsigned, -- 外键: source_page的主ID
	`page_box_id` bigint(20) unsigned, -- 外键: page_box的主ID
	`title` text, -- page标题
	`url` text, -- page url
	`tip` text, -- page的标注
	`user_id` bigint(20) unsigned DEFAULT '0', -- page的收藏者
	`date` datetime DEFAULT '0000-00-00 00:00:00', -- page的收藏时间
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;




-- ----------------------------
-- create page_box table(每个用户自己的page分类)
-- ----------------------------
DROP TABLE IF EXISTS `page_box`;
CREATE TABLE `page_box` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`name` text, -- page_box_name
	`content` text, -- page_box描述
	`user_id` bigint(20) unsigned DEFAULT '0', -- page_box的创建者
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;



-- ----------------------------
-- create clip table
-- ----------------------------
DROP TABLE IF EXISTS `clip`;
CREATE TABLE `clip` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`page_id` bigint(20) unsigned, -- 外键: page的主ID
	`content` longtext,
	`excerpt` text,
	`user_id` bigint(20) unsigned DEFAULT '0', -- clip的创建者
	`update_date` datetime DEFAULT '0000-00-00 00:00:00', -- clip创建的时间
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;


-- ----------------------------
-- create clip_box table(每个用户自己的clip分类)
-- ----------------------------
DROP TABLE IF EXISTS `clip_box`;
CREATE TABLE `clip_box` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`name` text, -- clip_box_name
	`content` text, -- clip_box描述
	`user_id` bigint(20) unsigned DEFAULT '0', -- clip_box的创建者
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;


-- ----------------------------
-- create clip_box_map table(clip、clip_box、user之间的映射关系)
-- ----------------------------
DROP TABLE IF EXISTS `clip_box_map`;
CREATE TABLE `clip_box_map` (
	`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	`clip_id` bigint(20) unsigned, -- 外键: clip的主ID
	`clip_box_id` bigint(20) unsigned, -- 外键: clip_box的主ID
	`user_id` bigint(20) unsigned DEFAULT '0', -- clip_box的创建者
	PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10000000 DEFAULT CHARSET=utf8;
