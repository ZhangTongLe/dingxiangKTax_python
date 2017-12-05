/*
Navicat MySQL Data Transfer

Source Server         : localmysql
Source Server Version : 50536
Source Host           : 127.0.0.1:3306
Source Database       : dingxiangktax

Target Server Type    : MYSQL
Target Server Version : 50536
File Encoding         : 65001

Date: 2017-12-03 15:04:20
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `countrytax`
-- ----------------------------
DROP TABLE IF EXISTS `countrytax`;
CREATE TABLE `countrytax` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Country_Title` varchar(255) DEFAULT NULL COMMENT '日期',
  `Country_Location` varchar(255) DEFAULT NULL COMMENT '位置',
  `Country_Data` date DEFAULT NULL COMMENT '日期',
  `Country_Type` varchar(255) DEFAULT NULL COMMENT '类型',
  `Country_Info` varchar(1000) DEFAULT NULL COMMENT '内容',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of countrytax
-- ----------------------------
