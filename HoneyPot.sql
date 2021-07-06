/*
 Navicat Premium Data Transfer

 Source Server         : macmysql
 Source Server Type    : MySQL
 Source Server Version : 80025
 Source Host           : localhost:3306
 Source Schema         : HoneyPot

 Target Server Type    : MySQL
 Target Server Version : 80025
 File Encoding         : 65001

 Date: 06/07/2021 22:50:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add threat', 7, 'add_threat');
INSERT INTO `auth_permission` VALUES (26, 'Can change threat', 7, 'change_threat');
INSERT INTO `auth_permission` VALUES (27, 'Can delete threat', 7, 'delete_threat');
INSERT INTO `auth_permission` VALUES (28, 'Can view threat', 7, 'view_threat');
INSERT INTO `auth_permission` VALUES (29, 'Can add threat ip', 8, 'add_threatip');
INSERT INTO `auth_permission` VALUES (30, 'Can change threat ip', 8, 'change_threatip');
INSERT INTO `auth_permission` VALUES (31, 'Can delete threat ip', 8, 'delete_threatip');
INSERT INTO `auth_permission` VALUES (32, 'Can view threat ip', 8, 'view_threatip');
INSERT INTO `auth_permission` VALUES (33, 'Can add threat type', 9, 'add_threattype');
INSERT INTO `auth_permission` VALUES (34, 'Can change threat type', 9, 'change_threattype');
INSERT INTO `auth_permission` VALUES (35, 'Can delete threat type', 9, 'delete_threattype');
INSERT INTO `auth_permission` VALUES (36, 'Can view threat type', 9, 'view_threattype');
INSERT INTO `auth_permission` VALUES (37, 'Can add captcha store', 10, 'add_captchastore');
INSERT INTO `auth_permission` VALUES (38, 'Can change captcha store', 10, 'change_captchastore');
INSERT INTO `auth_permission` VALUES (39, 'Can delete captcha store', 10, 'delete_captchastore');
INSERT INTO `auth_permission` VALUES (40, 'Can view captcha store', 10, 'view_captchastore');
COMMIT;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for captcha_captchastore
-- ----------------------------
DROP TABLE IF EXISTS `captcha_captchastore`;
CREATE TABLE `captcha_captchastore` (
  `id` int NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) NOT NULL,
  `response` varchar(32) NOT NULL,
  `hashkey` varchar(40) NOT NULL,
  `expiration` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashkey` (`hashkey`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of captcha_captchastore
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (10, 'captcha', 'captchastore');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (7, 'home', 'threat');
INSERT INTO `django_content_type` VALUES (8, 'home', 'threatip');
INSERT INTO `django_content_type` VALUES (9, 'home', 'threattype');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2021-07-06 11:37:09.857922');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2021-07-06 11:37:10.027556');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2021-07-06 11:37:10.204844');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2021-07-06 11:37:10.257650');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2021-07-06 11:37:10.269320');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2021-07-06 11:37:10.332237');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2021-07-06 11:37:10.365776');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2021-07-06 11:37:10.390205');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2021-07-06 11:37:10.401064');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2021-07-06 11:37:10.435093');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2021-07-06 11:37:10.438373');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2021-07-06 11:37:10.449409');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2021-07-06 11:37:10.488556');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2021-07-06 11:37:10.525312');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2021-07-06 11:37:10.547382');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2021-07-06 11:37:10.559016');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2021-07-06 11:37:10.600513');
INSERT INTO `django_migrations` VALUES (18, 'captcha', '0001_initial', '2021-07-06 11:37:10.623091');
INSERT INTO `django_migrations` VALUES (19, 'home', '0001_initial', '2021-07-06 11:37:10.664611');
INSERT INTO `django_migrations` VALUES (20, 'sessions', '0001_initial', '2021-07-06 11:37:10.677103');
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
INSERT INTO `django_session` VALUES ('6qj1z8r7mpl29b5yh106rwimechwdeo4', 'eyJpc19sb2dpbiI6dHJ1ZX0:1m0kXH:x5CwIJeyJRbS-cRr8B-ZvVqp1LrYDaZWDpz6be2zvU8', '2021-07-20 12:50:47.586252');
INSERT INTO `django_session` VALUES ('bfg91qlalxktfy1gufudl71xr19v3dky', 'eyJpc19sb2dpbiI6dHJ1ZX0:1m0kQv:j_JPR6gSLTdtWoP78jiMPlxtTyw5rJ2EAo-gz9NQ5OE', '2021-07-20 12:44:13.980825');
COMMIT;

-- ----------------------------
-- Table structure for home_threat
-- ----------------------------
DROP TABLE IF EXISTS `home_threat`;
CREATE TABLE `home_threat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `honeyPotID` int NOT NULL,
  `honeyPotType` int NOT NULL,
  `ip` varchar(30) NOT NULL,
  `origin` varchar(100) NOT NULL,
  `time` varchar(30) NOT NULL,
  `detail` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of home_threat
-- ----------------------------
BEGIN;
INSERT INTO `home_threat` VALUES (7, 1, 1, '127.0.0.1', '局域网', '2021-07-06 11:51:24', '非法密码尝试\n用户名：ac1d\n密码: 123456');
INSERT INTO `home_threat` VALUES (9, 1, 1, '127.0.0.1', '局域网', '2021-07-06 11:52:50', '非法密码尝试\n用户名：ac1d\n密码: 123456');
INSERT INTO `home_threat` VALUES (10, 1, 1, '127.0.0.1', '局域网', '2021-07-06 11:53:48', '非法密码尝试\n用户名：ac1d\n密码: 123456');
INSERT INTO `home_threat` VALUES (11, 1, 1, '127.0.0.1', '局域网', '2021-07-06 11:54:37', '非法密码尝试\n用户名：ac1d\n密码: 123456');
INSERT INTO `home_threat` VALUES (12, 1, 1, '127.0.0.1', '局域网', '2021-07-06 11:55:01', '非法密码尝试\n用户名：ac1d\n密码: 123456');
INSERT INTO `home_threat` VALUES (13, 1, 1, '127.0.0.1', '局域网', '2021-07-06 11:55:33', '非法密码尝试\n用户名：ac1d\n密码: 123456');
INSERT INTO `home_threat` VALUES (14, 1, 1, '127.0.0.1', '局域网', '2021-07-06 11:55:54', '非法密码尝试\n用户名：ac1d\n密码: 123456');
INSERT INTO `home_threat` VALUES (15, 1, 1, '127.0.0.1', '局域网', '2021-07-06 11:56:46', '非法密码尝试\n用户名：ac1d\n密码: 123456');
INSERT INTO `home_threat` VALUES (16, 1, 1, '127.0.0.1', '局域网', '2021-07-06 11:56:51', '非法密码尝试\n用户名：ac1d\n密码: 123456');
INSERT INTO `home_threat` VALUES (17, 1, 1, '172.17.0.1', '局域网', '2021-07-06 12:08:43', '非法密码尝试\n用户名：oho\n密码: ohoo');
INSERT INTO `home_threat` VALUES (18, 1, 1, '172.17.0.1', '局域网', '2021-07-06 12:09:30', '非法密码尝试\n用户名：oho\n密码: ohoo');
INSERT INTO `home_threat` VALUES (19, 1, 1, '172.17.0.1', '局域网', '2021-07-06 12:20:28', '非法密码尝试\n用户名：oho\n密码: ohoo');
INSERT INTO `home_threat` VALUES (20, 1, 1, '172.17.0.1', '局域网', '2021-07-06 12:20:49', '非法密码尝试\n用户名：oho\n密码: ohoo');
INSERT INTO `home_threat` VALUES (21, 1, 1, '172.17.0.1', '局域网', '2021-07-06 12:21:18', '非法密码尝试\n用户名：oho\n密码: ohoo');
INSERT INTO `home_threat` VALUES (22, 1, 1, '172.17.0.1', '局域网', '2021-07-06 12:21:47', '非法密码尝试\n用户名：oho\n密码: ohoo');
INSERT INTO `home_threat` VALUES (23, 1, 1, '172.17.0.1', '局域网', '2021-07-06 20:24:11', '非法密码尝试\n用户名：ASR\n密码: ASR');
INSERT INTO `home_threat` VALUES (24, 1, 1, '172.17.0.1', '局域网', '2021-07-06 22:44:10', '非法密码尝试\n用户名：asfasf\n密码: saggasg');
COMMIT;

-- ----------------------------
-- Table structure for home_threatip
-- ----------------------------
DROP TABLE IF EXISTS `home_threatip`;
CREATE TABLE `home_threatip` (
  `ip` varchar(30) NOT NULL,
  `origin` varchar(100) NOT NULL,
  `num` int NOT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of home_threatip
-- ----------------------------
BEGIN;
INSERT INTO `home_threatip` VALUES ('127.0.0.1', '局域网', 6);
INSERT INTO `home_threatip` VALUES ('172.17.0.1', '局域网', 8);
COMMIT;

-- ----------------------------
-- Table structure for home_threattype
-- ----------------------------
DROP TABLE IF EXISTS `home_threattype`;
CREATE TABLE `home_threattype` (
  `threatID` int NOT NULL,
  `num` int NOT NULL,
  PRIMARY KEY (`threatID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of home_threattype
-- ----------------------------
BEGIN;
INSERT INTO `home_threattype` VALUES (1, 20);
INSERT INTO `home_threattype` VALUES (2, 0);
INSERT INTO `home_threattype` VALUES (3, 0);
INSERT INTO `home_threattype` VALUES (4, 0);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
