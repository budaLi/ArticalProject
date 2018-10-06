/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50719
Source Host           : 127.0.0.1:3306
Source Database       : artile_spider

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2018-10-06 11:58:38
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `shixiseng`
-- ----------------------------
DROP TABLE IF EXISTS `shixiseng`;
CREATE TABLE `shixiseng` (
  `url` varchar(100) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `url_object_id` varchar(100) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `title` varchar(100) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `upgrade_time` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `salary_min` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `salary_max` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `job_city` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `degree_need` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `work_perweek` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `shixi_time` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `job_addvantage` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `job_info` longtext COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `company_name` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `company_url` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `work_address` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `tags` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `need_nums` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `end_time` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `crawl_time` date DEFAULT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;

-- ----------------------------
-- Records of shixiseng
-- ----------------------------
