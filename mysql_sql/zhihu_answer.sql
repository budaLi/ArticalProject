/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50719
Source Host           : 127.0.0.1:3306
Source Database       : artile_spider

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2018-10-06 11:58:22
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `zhihu_answer`
-- ----------------------------
DROP TABLE IF EXISTS `zhihu_answer`;
CREATE TABLE `zhihu_answer` (
  `zhihu_id` bigint(20) NOT NULL,
  `url` varchar(300) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `question_id` bigint(20) NOT NULL,
  `author_id` varchar(200) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `content` longtext COLLATE utf8mb4_vietnamese_ci,
  `praise_num` int(11) DEFAULT '0',
  `comment_num` int(11) DEFAULT '0',
  `create_time` date DEFAULT NULL,
  `update_time` date DEFAULT NULL,
  `crawl_time` datetime DEFAULT NULL,
  `crawl_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;

-- ----------------------------
-- Records of zhihu_answer
-- ----------------------------
