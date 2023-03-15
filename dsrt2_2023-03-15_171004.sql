/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
DROP TABLE IF EXISTS auth_group;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS auth_group_permissions;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS auth_permission;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS auth_user;
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

DROP TABLE IF EXISTS auth_user_groups;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS auth_user_user_permissions;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS django_admin_log;
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

DROP TABLE IF EXISTS django_content_type;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS django_migrations;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS django_session;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS image_data;
CREATE TABLE `image_data` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `file_name` varchar(255) DEFAULT NULL COMMENT '文件名',
  `file_path` varchar(255) DEFAULT NULL COMMENT '文件路径',
  `time_begin` datetime DEFAULT NULL COMMENT '开始时间',
  `time_end` datetime DEFAULT NULL COMMENT '结束时间',
  `freq` double DEFAULT NULL COMMENT '频率',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='成像文件';

DROP TABLE IF EXISTS project_data;
CREATE TABLE `project_data` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `file_name` varchar(255) DEFAULT NULL COMMENT '文件名',
  `file_path` varchar(255) DEFAULT NULL COMMENT '文件路径',
  `date` date DEFAULT NULL COMMENT '日期',
  `direct` varchar(2) DEFAULT NULL COMMENT '投影方向',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='投影预览文件';

DROP TABLE IF EXISTS spec_data;
CREATE TABLE `spec_data` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `file_name` varchar(255) DEFAULT NULL COMMENT '文件名',
  `file_path` varchar(255) DEFAULT NULL COMMENT '文件路径',
  `time_begin` datetime DEFAULT NULL COMMENT '开始时间',
  `time_end` datetime DEFAULT NULL COMMENT '结束时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='频谱数据文件';

DROP TABLE IF EXISTS spec_view;
CREATE TABLE `spec_view` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `file_name` varchar(255) DEFAULT NULL COMMENT '文件名',
  `file_path` varchar(255) DEFAULT NULL COMMENT '文件路径',
  `date` date DEFAULT NULL COMMENT '日期',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='频谱概图文件';



INSERT INTO auth_permission(id,name,content_type_id,codename) VALUES(1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session');





INSERT INTO django_content_type(id,app_label,model) VALUES(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');

INSERT INTO django_migrations(id,app,name,applied) VALUES(1,'contenttypes','0001_initial','2023-03-07 05:29:25.773252'),(2,'auth','0001_initial','2023-03-07 05:29:26.419047'),(3,'admin','0001_initial','2023-03-07 05:29:26.582390'),(4,'admin','0002_logentry_remove_auto_add','2023-03-07 05:29:26.592647'),(5,'admin','0003_logentry_add_action_flag_choices','2023-03-07 05:29:26.602150'),(6,'contenttypes','0002_remove_content_type_name','2023-03-07 05:29:26.690819'),(7,'auth','0002_alter_permission_name_max_length','2023-03-07 05:29:26.755693'),(8,'auth','0003_alter_user_email_max_length','2023-03-07 05:29:26.786530'),(9,'auth','0004_alter_user_username_opts','2023-03-07 05:29:26.796535'),(10,'auth','0005_alter_user_last_login_null','2023-03-07 05:29:26.854069'),(11,'auth','0006_require_contenttypes_0002','2023-03-07 05:29:26.858571'),(12,'auth','0007_alter_validators_add_error_messages','2023-03-07 05:29:26.868525'),(13,'auth','0008_alter_user_username_max_length','2023-03-07 05:29:26.937072'),(14,'auth','0009_alter_user_last_name_max_length','2023-03-07 05:29:27.000833'),(15,'auth','0010_alter_group_name_max_length','2023-03-07 05:29:27.024751'),(16,'auth','0011_update_proxy_permissions','2023-03-07 05:29:27.037656'),(17,'auth','0012_alter_user_first_name_max_length','2023-03-07 05:29:27.107693'),(18,'sessions','0001_initial','2023-03-07 05:29:27.154239');


INSERT INTO image_data(id,file_name,file_path,time_begin,time_end,freq) VALUES(3,'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits','/home/gytide/dsrtprod/data/2023/03/dsrtimg/ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits','2022-04-17 03:26:00','2022-04-17 03:39:59',233);

INSERT INTO project_data(id,file_name,file_path,date,direct) VALUES(1,'PRO20230301.fits','/home/gytide/dsrtprod/data/2023/03/project_image','2023-03-01','EW'),(2,'PRO20230301.fits','/home/gytide/dsrtprod/data/2023/03/project_image','2023-04-02','EW');

INSERT INTO spec_data(id,file_name,file_path,time_begin,time_end) VALUES(1,'ODACH_CART05_SRSP_L1_STP_20220417061006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417061006_V01.01.fits','2022-04-17 06:10:06','2022-04-17 06:15:05'),(2,'ODACH_CART05_SRSP_L1_STP_20220417060517_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417060517_V01.01.fits','2022-04-17 06:05:17','2022-04-17 06:10:05'),(3,'ODACH_CART05_SRSP_L1_STP_20220417083505_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417083505_V01.01.fits','2022-04-17 08:35:06','2022-04-17 08:39:50'),(4,'ODACH_CART05_SRSP_L1_STP_20220417015006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417015006_V01.01.fits','2022-04-17 01:50:07','2022-04-17 01:55:06'),(5,'ODACH_CART05_SRSP_L1_STP_20220417084006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417084006_V01.01.fits','2022-04-17 08:40:06','2022-04-17 08:45:05'),(6,'ODACH_CART05_SRSP_L1_STP_20220417072006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417072006_V01.01.fits','2022-04-17 07:20:06','2022-04-17 07:25:05'),(7,'ODACH_CART05_SRSP_L1_STP_20220417074006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417074006_V01.01.fits','2022-04-17 07:40:06','2022-04-17 07:45:05'),(8,'ODACH_CART05_SRSP_L1_STP_20220417011506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417011506_V01.01.fits','2022-04-17 01:15:07','2022-04-17 01:20:06'),(9,'ODACH_CART05_SRSP_L1_STP_20220417064506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417064506_V01.01.fits','2022-04-17 06:45:06','2022-04-17 06:50:05'),(10,'ODACH_CART05_SRSP_L1_STP_20220417073520_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417073520_V01.01.fits','2022-04-17 07:35:20','2022-04-17 07:40:05'),(11,'ODACH_CART05_SRSP_L1_STP_20220417094008_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417094008_V01.01.fits','2022-04-17 09:40:08','2022-04-17 09:45:06'),(12,'ODACH_CART05_SRSP_L1_STP_20220417075006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417075006_V01.01.fits','2022-04-17 07:50:07','2022-04-17 07:55:06'),(13,'ODACH_CART05_SRSP_L1_STP_20220417051006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417051006_V01.01.fits','2022-04-17 05:10:06','2022-04-17 05:15:05'),(14,'ODACH_CART05_SRSP_L1_STP_20220417063518_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417063518_V01.01.fits','2022-04-17 06:35:18','2022-04-17 06:40:06'),(15,'ODACH_CART05_SRSP_L1_STP_20220417084506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417084506_V01.01.fits','2022-04-17 08:45:07','2022-04-17 08:50:06'),(16,'ODACH_CART05_SRSP_L1_STP_20220417054007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417054007_V01.01.fits','2022-04-17 05:40:07','2022-04-17 05:45:04'),(17,'ODACH_CART05_SRSP_L1_STP_20220417072506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417072506_V01.01.fits','2022-04-17 07:25:06','2022-04-17 07:30:05'),(18,'ODACH_CART05_SRSP_L1_STP_20220417063006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417063006_V01.01.fits','2022-04-17 06:30:07','2022-04-17 06:35:02'),(19,'ODACH_CART05_SRSP_L1_STP_20220417002505_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417002505_V01.01.fits','2022-04-17 00:25:06','2022-04-17 00:30:05'),(20,'ODACH_CART05_SRSP_L1_STP_20220417071006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417071006_V01.01.fits','2022-04-17 07:10:07','2022-04-17 07:15:06'),(21,'ODACH_CART05_SRSP_L1_STP_20220417093506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417093506_V01.01.fits','2022-04-17 09:35:06','2022-04-17 09:39:52'),(22,'ODACH_CART05_SRSP_L1_STP_20220417100507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417100507_V01.01.fits','2022-04-17 10:05:07','2022-04-17 10:09:53'),(23,'ODACH_CART05_SRSP_L1_STP_20220417015507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417015507_V01.01.fits','2022-04-17 01:55:07','2022-04-17 02:00:04'),(24,'ODACH_CART05_SRSP_L1_STP_20220417021006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417021006_V01.01.fits','2022-04-17 02:10:07','2022-04-17 02:15:06'),(25,'ODACH_CART05_SRSP_L1_STP_20220417002007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417002007_V01.01.fits','2022-04-17 00:20:07','2022-04-17 00:25:04'),(26,'ODACH_CART05_SRSP_L1_STP_20220417050006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417050006_V01.01.fits','2022-04-17 05:00:07','2022-04-17 05:04:59'),(27,'ODACH_CART05_SRSP_L1_STP_20220417051506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417051506_V01.01.fits','2022-04-17 05:15:07','2022-04-17 05:20:05'),(28,'ODACH_CART05_SRSP_L1_STP_20220417014506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417014506_V01.01.fits','2022-04-17 01:45:06','2022-04-17 01:50:05'),(29,'ODACH_CART05_SRSP_L1_STP_20220417043514_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417043514_V01.01.fits','2022-04-17 04:35:14','2022-04-17 04:40:05'),(30,'ODACH_CART05_SRSP_L1_STP_20220417090506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417090506_V01.01.fits','2022-04-17 09:05:07','2022-04-17 09:09:51'),(31,'ODACH_CART05_SRSP_L1_STP_20220417050515_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417050515_V01.01.fits','2022-04-17 05:05:15','2022-04-17 05:10:05'),(32,'ODACH_CART05_SRSP_L1_STP_20220417044507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417044507_V01.01.fits','2022-04-17 04:45:07','2022-04-17 04:50:04'),(33,'ODACH_CART05_SRSP_L1_STP_20220417053516_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417053516_V01.01.fits','2022-04-17 05:35:16','2022-04-17 05:40:06'),(34,'ODACH_CART05_SRSP_L1_STP_20220417021507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417021507_V01.01.fits','2022-04-17 02:15:07','2022-04-17 02:20:04'),(35,'ODACH_CART05_SRSP_L1_STP_20220417081007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417081007_V01.01.fits','2022-04-17 08:10:07','2022-04-17 08:15:04'),(36,'ODACH_CART05_SRSP_L1_STP_20220417092507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417092507_V01.01.fits','2022-04-17 09:25:07','2022-04-17 09:30:04'),(37,'ODACH_CART05_SRSP_L1_STP_20220417093005_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417093005_V01.01.fits','2022-04-17 09:30:06','2022-04-17 09:35:05'),(38,'ODACH_CART05_SRSP_L1_STP_20220417060007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417060007_V01.01.fits','2022-04-17 06:00:07','2022-04-17 06:05:01'),(39,'ODACH_CART05_SRSP_L1_STP_20220417095005_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417095005_V01.01.fits','2022-04-17 09:50:06','2022-04-17 09:55:05'),(40,'ODACH_CART05_SRSP_L1_STP_20220417040513_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417040513_V01.01.fits','2022-04-17 04:05:13','2022-04-17 04:10:04'),(41,'ODACH_CART05_SRSP_L1_STP_20220417085506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417085506_V01.01.fits','2022-04-17 08:55:06','2022-04-17 09:00:05'),(42,'ODACH_CART05_SRSP_L1_STP_20220417045006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417045006_V01.01.fits','2022-04-17 04:50:06','2022-04-17 04:55:05'),(43,'ODACH_CART05_SRSP_L1_STP_20220417033512_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417033512_V01.01.fits','2022-04-17 03:35:13','2022-04-17 03:40:05'),(44,'ODACH_CART05_SRSP_L1_STP_20220417035506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417035506_V01.01.fits','2022-04-17 03:55:06','2022-04-17 04:00:05'),(45,'ODACH_CART05_SRSP_L1_STP_20220417080521_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417080521_V01.01.fits','2022-04-17 08:05:21','2022-04-17 08:10:05'),(46,'ODACH_CART05_SRSP_L1_STP_20220417094507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417094507_V01.01.fits','2022-04-17 09:45:07','2022-04-17 09:50:04'),(47,'ODACH_CART05_SRSP_L1_STP_20220417100006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417100006_V01.01.fits','2022-04-17 10:00:07','2022-04-17 10:05:06'),(48,'ODACH_CART05_SRSP_L1_STP_20220417070519_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417070519_V01.01.fits','2022-04-17 07:05:19','2022-04-17 07:10:05'),(49,'ODACH_CART05_SRSP_L1_STP_20220417062506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417062506_V01.01.fits','2022-04-17 06:25:06','2022-04-17 06:30:05'),(50,'ODACH_CART05_SRSP_L1_STP_20220417001506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417001506_V01.01.fits','2022-04-17 00:15:07','2022-04-17 00:20:05'),(51,'ODACH_CART05_SRSP_L1_STP_20220417092006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417092006_V01.01.fits','2022-04-17 09:20:07','2022-04-17 09:25:05'),(52,'ODACH_CART05_SRSP_L1_STP_20220417031505_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417031505_V01.01.fits','2022-04-17 03:15:06','2022-04-17 03:20:05'),(53,'ODACH_CART05_SRSP_L1_STP_20220417043005_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417043005_V01.01.fits','2022-04-17 04:30:06','2022-04-17 04:34:58'),(54,'ODACH_CART05_SRSP_L1_STP_20220417030006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417030006_V01.01.fits','2022-04-17 03:00:06','2022-04-17 03:04:55'),(55,'ODACH_CART05_SRSP_L1_STP_20220417020509_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417020509_V01.01.fits','2022-04-17 02:05:10','2022-04-17 02:10:05'),(56,'ODACH_CART05_SRSP_L1_STP_20220417000505_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417000505_V01.01.fits','2022-04-17 00:05:06','2022-04-17 00:10:05'),(57,'ODACH_CART05_SRSP_L1_STP_20220417091506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417091506_V01.01.fits','2022-04-17 09:15:06','2022-04-17 09:20:05'),(58,'ODACH_CART05_SRSP_L1_STP_20220417052505_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417052505_V01.01.fits','2022-04-17 05:25:06','2022-04-17 05:30:05'),(59,'ODACH_CART05_SRSP_L1_STP_20220417034506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417034506_V01.01.fits','2022-04-17 03:45:07','2022-04-17 03:50:06'),(60,'ODACH_CART05_SRSP_L1_STP_20220417023510_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417023510_V01.01.fits','2022-04-17 02:35:11','2022-04-17 02:40:05'),(61,'ODACH_CART05_SRSP_L1_STP_20220417081505_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417081505_V01.01.fits','2022-04-17 08:15:06','2022-04-17 08:20:05'),(62,'ODACH_CART05_SRSP_L1_STP_20220417082506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417082506_V01.01.fits','2022-04-17 08:25:07','2022-04-17 08:30:06'),(63,'ODACH_CART05_SRSP_L1_STP_20220417062007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417062007_V01.01.fits','2022-04-17 06:20:07','2022-04-17 06:25:05'),(64,'ODACH_CART05_SRSP_L1_STP_20220417090006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417090006_V01.01.fits','2022-04-17 09:00:07','2022-04-17 09:05:05'),(65,'ODACH_CART05_SRSP_L1_STP_20220417003006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417003006_V01.01.fits','2022-04-17 00:30:06','2022-04-17 00:34:51'),(66,'ODACH_CART05_SRSP_L1_STP_20220417004506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417004506_V01.01.fits','2022-04-17 00:45:06','2022-04-17 00:50:05'),(67,'ODACH_CART05_SRSP_L1_STP_20220417030511_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417030511_V01.01.fits','2022-04-17 03:05:12','2022-04-17 03:10:06'),(68,'ODACH_CART05_SRSP_L1_STP_20220417005006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417005006_V01.01.fits','2022-04-17 00:50:06','2022-04-17 00:55:05'),(69,'ODACH_CART05_SRSP_L1_STP_20220417073006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417073006_V01.01.fits','2022-04-17 07:30:07','2022-04-17 07:35:04'),(70,'ODACH_CART05_SRSP_L1_STP_20220417024506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417024506_V01.01.fits','2022-04-17 02:45:07','2022-04-17 02:50:05'),(71,'ODACH_CART05_SRSP_L1_STP_20220417025505_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417025505_V01.01.fits','2022-04-17 02:55:06','2022-04-17 03:00:05'),(72,'ODACH_CART05_SRSP_L1_STP_20220417045506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417045506_V01.01.fits','2022-04-17 04:55:06','2022-04-17 05:00:05'),(73,'ODACH_CART05_SRSP_L1_STP_20220417075507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417075507_V01.01.fits','2022-04-17 07:55:07','2022-04-17 08:00:05'),(74,'ODACH_CART05_SRSP_L1_STP_20220417032506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417032506_V01.01.fits','2022-04-17 03:25:07','2022-04-17 03:30:06'),(75,'ODACH_CART05_SRSP_L1_STP_20220417010507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417010507_V01.01.fits','2022-04-17 01:05:08','2022-04-17 01:10:05'),(76,'ODACH_CART05_SRSP_L1_STP_20220417052007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417052007_V01.01.fits','2022-04-17 05:20:07','2022-04-17 05:25:04'),(77,'ODACH_CART05_SRSP_L1_STP_20220417080006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417080006_V01.01.fits','2022-04-17 08:00:06','2022-04-17 08:05:05'),(78,'ODACH_CART05_SRSP_L1_STP_20220417011006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417011006_V01.01.fits','2022-04-17 01:10:07','2022-04-17 01:15:05'),(79,'ODACH_CART05_SRSP_L1_STP_20220417024006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417024006_V01.01.fits','2022-04-17 02:40:06','2022-04-17 02:45:05'),(80,'ODACH_CART05_SRSP_L1_STP_20220417022506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417022506_V01.01.fits','2022-04-17 02:25:07','2022-04-17 02:30:05'),(81,'ODACH_CART05_SRSP_L1_STP_20220417040006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417040006_V01.01.fits','2022-04-17 04:00:07','2022-04-17 04:04:57'),(82,'ODACH_CART05_SRSP_L1_STP_20220417012506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417012506_V01.01.fits','2022-04-17 01:25:06','2022-04-17 01:30:05'),(83,'ODACH_CART05_SRSP_L1_STP_20220417031007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417031007_V01.01.fits','2022-04-17 03:10:07','2022-04-17 03:15:04'),(84,'ODACH_CART05_SRSP_L1_STP_20220417005506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417005506_V01.01.fits','2022-04-17 00:55:07','2022-04-17 01:00:06'),(85,'ODACH_CART05_SRSP_L1_STP_20220417042507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417042507_V01.01.fits','2022-04-17 04:25:07','2022-04-17 04:30:04'),(86,'ODACH_CART05_SRSP_L1_STP_20220417033007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417033007_V01.01.fits','2022-04-17 03:30:07','2022-04-17 03:34:56'),(87,'ODACH_CART05_SRSP_L1_STP_20220417101009_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417101009_V01.01.fits','2022-04-17 10:10:09','2022-04-17 10:15:05'),(88,'ODACH_CART05_SRSP_L1_STP_20220417044006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417044006_V01.01.fits','2022-04-17 04:40:07','2022-04-17 04:45:06'),(89,'ODACH_CART05_SRSP_L1_STP_20220417064007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417064007_V01.01.fits','2022-04-17 06:40:07','2022-04-17 06:45:05'),(90,'ODACH_CART05_SRSP_L1_STP_20220417083007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417083007_V01.01.fits','2022-04-17 08:30:07','2022-04-17 08:35:04'),(91,'ODACH_CART05_SRSP_L1_STP_20220417101506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417101506_V01.01.fits','2022-04-17 10:15:06','2022-04-17 10:20:05'),(92,'ODACH_CART05_SRSP_L1_STP_20220417055506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417055506_V01.01.fits','2022-04-17 05:55:07','2022-04-17 06:00:06'),(93,'ODACH_CART05_SRSP_L1_STP_20220417085007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417085007_V01.01.fits','2022-04-17 08:50:07','2022-04-17 08:55:04'),(94,'ODACH_CART05_SRSP_L1_STP_20220417010007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417010007_V01.01.fits','2022-04-17 01:00:07','2022-04-17 01:04:52'),(95,'ODACH_CART05_SRSP_L1_STP_20220417035007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417035007_V01.01.fits','2022-04-17 03:50:07','2022-04-17 03:55:05'),(96,'ODACH_CART05_SRSP_L1_STP_20220417020006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417020006_V01.01.fits','2022-04-17 02:00:06','2022-04-17 02:04:54'),(97,'ODACH_CART05_SRSP_L1_STP_20220417013508_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417013508_V01.01.fits','2022-04-17 01:35:09','2022-04-17 01:40:04'),(98,'ODACH_CART05_SRSP_L1_STP_20220417082006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417082006_V01.01.fits','2022-04-17 08:20:06','2022-04-17 08:25:05'),(99,'ODACH_CART05_SRSP_L1_STP_20220417004007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417004007_V01.01.fits','2022-04-17 00:40:07','2022-04-17 00:45:04'),(100,'ODACH_CART05_SRSP_L1_STP_20220417023006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417023006_V01.01.fits','2022-04-17 02:30:07','2022-04-17 02:34:55'),(101,'ODACH_CART05_SRSP_L1_STP_20220417053006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417053006_V01.01.fits','2022-04-17 05:30:06','2022-04-17 05:35:00'),(102,'ODACH_CART05_SRSP_L1_STP_20220417054505_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417054505_V01.01.fits','2022-04-17 05:45:06','2022-04-17 05:50:05'),(103,'ODACH_CART05_SRSP_L1_STP_20220417032006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417032006_V01.01.fits','2022-04-17 03:20:06','2022-04-17 03:25:05'),(104,'ODACH_CART05_SRSP_L1_STP_20220417071507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417071507_V01.01.fits','2022-04-17 07:15:07','2022-04-17 07:20:04'),(105,'ODACH_CART05_SRSP_L1_STP_20220417091007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417091007_V01.01.fits','2022-04-17 09:10:07','2022-04-17 09:15:05'),(106,'ODACH_CART05_SRSP_L1_STP_20220417074506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417074506_V01.01.fits','2022-04-17 07:45:07','2022-04-17 07:50:05'),(107,'ODACH_CART05_SRSP_L1_STP_20220417065006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417065006_V01.01.fits','2022-04-17 06:50:07','2022-04-17 06:55:05'),(108,'ODACH_CART05_SRSP_L1_STP_20220417102006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417102006_V01.01.fits','2022-04-17 10:20:07','2022-04-17 10:25:06'),(109,'ODACH_CART05_SRSP_L1_STP_20220417061506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417061506_V01.01.fits','2022-04-17 06:15:07','2022-04-17 06:20:06'),(110,'ODACH_CART05_SRSP_L1_STP_20220417034006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417034006_V01.01.fits','2022-04-17 03:40:07','2022-04-17 03:45:05'),(111,'ODACH_CART05_SRSP_L1_STP_20220417003506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417003506_V01.01.fits','2022-04-17 00:35:07','2022-04-17 00:40:06'),(112,'ODACH_CART05_SRSP_L1_STP_20220417013006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417013006_V01.01.fits','2022-04-17 01:30:07','2022-04-17 01:34:53'),(113,'ODACH_CART05_SRSP_L1_STP_20220417095506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417095506_V01.01.fits','2022-04-17 09:55:06','2022-04-17 10:00:05'),(114,'ODACH_CART05_SRSP_L1_STP_20220417055006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417055006_V01.01.fits','2022-04-17 05:50:06','2022-04-17 05:55:05'),(115,'ODACH_CART05_SRSP_L1_STP_20220417070005_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417070005_V01.01.fits','2022-04-17 07:00:06','2022-04-17 07:05:03'),(116,'ODACH_CART05_SRSP_L1_STP_20220417012007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417012007_V01.01.fits','2022-04-17 01:20:07','2022-04-17 01:25:05'),(117,'ODACH_CART05_SRSP_L1_STP_20220417065507_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417065507_V01.01.fits','2022-04-17 06:55:07','2022-04-17 07:00:04'),(118,'ODACH_CART05_SRSP_L1_STP_20220417025007_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417025007_V01.01.fits','2022-04-17 02:50:07','2022-04-17 02:55:04'),(119,'ODACH_CART05_SRSP_L1_STP_20220417041506_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417041506_V01.01.fits','2022-04-17 04:15:06','2022-04-17 04:20:05'),(120,'ODACH_CART05_SRSP_L1_STP_20220417042006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417042006_V01.01.fits','2022-04-17 04:20:07','2022-04-17 04:25:06'),(121,'ODACH_CART05_SRSP_L1_STP_20220417041005_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417041005_V01.01.fits','2022-04-17 04:10:06','2022-04-17 04:15:05'),(122,'ODACH_CART05_SRSP_L1_STP_20220417022006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417022006_V01.01.fits','2022-04-17 02:20:06','2022-04-17 02:25:05'),(123,'ODACH_CART05_SRSP_L1_STP_20220417001006_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417001006_V01.01.fits','2022-04-17 00:10:06','2022-04-17 00:15:05'),(124,'ODACH_CART05_SRSP_L1_STP_20220417014005_V01.01.fits','/home/gytide/dsrtprod/data/2023/03/dsrtspe/ODACH_CART05_SRSP_L1_STP_20220417014005_V01.01.fits','2022-04-17 01:40:06','2022-04-17 01:45:05');
INSERT INTO spec_view(id,file_name,file_path,date) VALUES(1,'SPE20220301.fits','/home/gytide/dsrtprod/data/2023/03/speview','2023-03-01'),(2,'SPE20220301.fits','/home/gytide/dsrtprod/data/2023/03/speview','2023-04-02');