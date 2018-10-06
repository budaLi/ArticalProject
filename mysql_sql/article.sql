/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50719
Source Host           : 127.0.0.1:3306
Source Database       : artile_spider

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2018-10-06 11:58:11
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `article`
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `title` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_mysql500_ci NOT NULL COMMENT '标题',
  `create_date` date DEFAULT NULL COMMENT '创建日期',
  `url` varchar(300) COLLATE utf8mb4_vietnamese_ci NOT NULL COMMENT '网页链接',
  `url_object_id` varchar(50) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `front_image_url` varchar(300) COLLATE utf8mb4_vietnamese_ci DEFAULT '',
  `front_image_path` varchar(300) COLLATE utf8mb4_vietnamese_ci DEFAULT '',
  `comment_nums` int(11) DEFAULT NULL,
  `fav_nums` int(11) DEFAULT NULL,
  `praise_nums` int(11) DEFAULT NULL,
  `tags` varchar(300) COLLATE utf8mb4_vietnamese_ci DEFAULT '' COMMENT '标签',
  `content` longtext COLLATE utf8mb4_vietnamese_ci,
  `crawl_time` date DEFAULT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;

-- ----------------------------
-- Records of article
-- ----------------------------
