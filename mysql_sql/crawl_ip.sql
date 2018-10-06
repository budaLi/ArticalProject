/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50719
Source Host           : 127.0.0.1:3306
Source Database       : artile_spider

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2018-10-06 11:58:00
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `crawl_ip`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_ip`;
CREATE TABLE `crawl_ip` (
  `ip_url` varchar(20) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `port` varchar(20) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `ip_type` varchar(20) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `speed` varchar(10) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  PRIMARY KEY (`ip_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;

-- ----------------------------
-- Records of crawl_ip
-- ----------------------------
