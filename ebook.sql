/*
Source Database       : ebook

Date: 2013-09-13 15:31:32
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `chapter`
-- ----------------------------
DROP TABLE IF EXISTS `chapter`;
CREATE TABLE `chapter` (
  `nid` varchar(100) NOT NULL,
  `cid` int(11) NOT NULL,
  `cTitle` varchar(255) NOT NULL,
  `bookName` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `imgCount` int(11) NOT NULL,
  PRIMARY KEY  (`nid`,`cid`),
  KEY `ni` USING BTREE (`nid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for `shotbook`
-- ----------------------------
DROP TABLE IF EXISTS `shotbook`;
CREATE TABLE `shotbook` (
  `nid` varchar(100) NOT NULL COMMENT '小说id',
  `jdid` varchar(30) default NULL,
  `bookName` varchar(100) NOT NULL COMMENT '小说名称',
  `author` varchar(100) NOT NULL COMMENT '小说作者',
  `coverImgPath` varchar(100) default NULL COMMENT '小说封面图片地址',
  `description` longtext COMMENT '小说简介',
  `type` varchar(100) NOT NULL COMMENT '小说类型',
  `chapterList` longtext NOT NULL COMMENT '章节列表',
  `chapterCount` int(11) NOT NULL COMMENT '章节总数',
  `imgCount` int(11) NOT NULL,
  `state` int(11) NOT NULL COMMENT '小说状态 0，为连载，1为完结',
  `createTime` varchar(100) NOT NULL,
  `updateTime` varchar(100) NOT NULL COMMENT '更新时间',
  `dohost` varchar(10) NOT NULL,
  `chapterok` int(11) NOT NULL,
  `isok` int(11) NOT NULL default '0' COMMENT '是否建到索引中去，0为没有，1为已经建了',
  PRIMARY KEY  (`nid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

