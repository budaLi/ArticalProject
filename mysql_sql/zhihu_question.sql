/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50719
Source Host           : 127.0.0.1:3306
Source Database       : artile_spider

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2018-10-06 11:58:28
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `zhihu_question`
-- ----------------------------
DROP TABLE IF EXISTS `zhihu_question`;
CREATE TABLE `zhihu_question` (
  `zhihu_id` bigint(20) NOT NULL,
  `topics` varchar(255) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `url` varchar(255) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `content` longtext COLLATE utf8mb4_vietnamese_ci,
  `create_time` date DEFAULT NULL,
  `update_time` date DEFAULT NULL,
  `answer_num` int(11) DEFAULT '0',
  `watch_user_num` int(11) DEFAULT '0',
  `comment_num` int(11) DEFAULT '0',
  `click_num` int(11) DEFAULT '0',
  `crawl_time` datetime NOT NULL,
  `crawl_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;

-- ----------------------------
-- Records of zhihu_question
-- ----------------------------
