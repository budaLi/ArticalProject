/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50719
Source Host           : 127.0.0.1:3306
Source Database       : movie

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2018-10-06 11:59:16
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `tc_movie`
-- ----------------------------
DROP TABLE IF EXISTS `tc_movie`;
CREATE TABLE `tc_movie` (
  `movie_name` varchar(100) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `short_desc` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `score` varchar(6) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `stars` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `hot` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `play_url` longtext COLLATE utf8mb4_vietnamese_ci,
  `image_url` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `image_path` varchar(200) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `alias` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `director` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `tags` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_vietnamese_ci,
  `play_time` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `crawl_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`movie_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;

-- ----------------------------
-- Records of tc_movie
-- ----------------------------
