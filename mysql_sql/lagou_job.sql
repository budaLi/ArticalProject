/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50719
Source Host           : 127.0.0.1:3306
Source Database       : artile_spider

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2018-10-06 11:57:41
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `lagou_job`
-- ----------------------------
DROP TABLE IF EXISTS `lagou_job`;
CREATE TABLE `lagou_job` (
  `title` varchar(300) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `url` varchar(300) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `url_object_id` varchar(300) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `salary_min` varchar(30) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `salary_max` varchar(30) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `job_city` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `work_years_min` varchar(30) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `work_years_max` varchar(30) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `degree_need` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `work_type` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `tags` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `publish_time` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `job_addvantage` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `job_desc` longtext COLLATE utf8mb4_vietnamese_ci,
  `company_name` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `company_area` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `company_develop_state` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `company_url` varchar(300) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `company_scale` varchar(100) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `crawl_time` date DEFAULT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;

-- ----------------------------
-- Records of lagou_job
-- ----------------------------
