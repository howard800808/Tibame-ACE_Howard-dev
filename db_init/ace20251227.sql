CREATE DATABASE  IF NOT EXISTS `ace` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ace`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ace
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_bin NOT NULL COMMENT '部門代碼',
  `name_zh` varchar(100) COLLATE utf8mb4_bin NOT NULL COMMENT '部門名稱(中文)',
  `name_en` varchar(100) COLLATE utf8mb4_bin NOT NULL COMMENT '部門名稱(英文)',
  `channel_access_token` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT 'LINE Bot Access Token',
  `channel_secret` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT 'LINE Bot Channel Secret',
  `created_at` datetime DEFAULT (now()) COMMENT '建立時間',
  `updated_at` datetime DEFAULT (now()) COMMENT '更新時間',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_departments_code` (`code`),
  KEY `ix_departments_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'GS','客務部','Guest Services','MxuOtBSYhdm1T0XMAHonGiiIyIlwzVQ+4sTxW25Grruzxlz3TC+q50mxkcmu9dnnqkq1e8RNKm0bKoGlQETCC1X0/JoIkhkBobcT4c1Mz97YyvTdGSYMFQnQC/EZ1xwZawymWJihprpaLteucQ6gqgdB04t89/1O/w1cDnyilFU=','ca87c1e2f974953a128e7dec4454f4fb','2025-12-27 22:45:23','2025-12-27 22:45:23'),(2,'HK','房務部','Housekeeping','HpQnEQnQkHnJrjUqnDhCf6VjDUbpFo3vfcgQmoIYRodHh41xBqKi5veh0ng/Fpb83O/bwMb2cl3PectuRXnFhAxUAQ9pOXXImUbhMrsDtX/Ojc8sjut7p8tm62eF7p9PBJHm0cjlU+4XvpQlBiukcgdB04t89/1O/w1cDnyilFU=','6484246f951afec8dacd6d3ca1f5056b','2025-12-27 22:45:23','2025-12-27 22:45:23'),(3,'CON','門房諮詢服務中心','Concierge','GgrwJ9o5Ob96ylf70vUr7yM1iJuyAG7UPWCJ0J7hsCrOXxZbKwuXdWSOmBxnP1VPgmfeEDe4NvF3yZQNnGYSVx/Zz/n/1YL6hHUHOx6NzKe/23rXNJYH9Fg0yrSwNri9xhOA4PlZhQBqaqWo1rnnzQdB04t89/1O/w1cDnyilFU=','bec44c0da0920af55cd2af04650c767e','2025-12-27 22:45:23','2025-12-27 22:45:23'),(4,'BP','烘焙點心房','Bakery & Pastry','p3IKt8qxi38bWa99f9zrFb7O1UNVioV2XspJTXcGOcDl5pGd6BvZiRb/ZiGYtpxweHz5IxaHdWHZ0+4YyBDK5UUTW6Nvr1js3jVa/AhvsODv66Gm17fq4r4PZh5U5FDZxeUesGiLuuXLNju5uTFkSwdB04t89/1O/w1cDnyilFU=','246b6237d02d448396b2d8f856827637','2025-12-27 22:45:23','2025-12-27 22:45:23'),(5,'FB','餐飲','Food & Beverage','HLK6AtfByF+obzujnta/XxhT9QD1JeDqYwFjiQryYRwXvKZvW3joLfS12EjI4LDyhsUYQTMFdNWEB2ocOkylOgVtTcaOPf51oFXYWbL6/ri9AVfWqDGMeD5J5q2+TtHzNE092UdhaT35zk85Pp3d6QdB04t89/1O/w1cDnyilFU=','43019aef0ed7626c454e1a02795da0cc','2025-12-27 22:45:23','2025-12-27 22:45:23'),(6,'CBS','會議宴會','Conference & Banquet Services','7iCPU+jjVueLE3GuWB/dBeJnocZD2ugA2S8vP82tocOqepa4wFWKr/jVww37EDk3Xhzr4OViyGYq0XvEpd8nexfpECEVBb0Iz5DQm+3KSex9rtQiNJ+GInCo2fisbsxcJ8wqIIAnvBJzPg5K+DU7kwdB04t89/1O/w1cDnyilFU=','1edff2612ed91a6821bcf393fee7ad97','2025-12-27 22:45:23','2025-12-27 22:45:23'),(7,'FS','花房','Flower Shop','QARjCy6uOvP55smmIUNiRSq0eTaUIfv3aQxvN6MZc0i/r+kTN1iAVDzpVi3irWWP1bIpeAGhQex8z9PKV133bSsWOYEjdu6QSJtqX+H0afzmoNfcD+Lyg2TVE1PmJCwVduZly9gvSIQOsQ5fPMPtuQdB04t89/1O/w1cDnyilFU=','1f99fae43459eb6eb1e8a58cb6ac1c96','2025-12-27 22:45:23','2025-12-27 22:45:23'),(8,'LUR','洗衣房與制服室','Laundry & Uniform Room','UwAvvI1P0oGbX+WaWFTVtVOWUVzEd99cVMuMSxkkvrY5/poKBxmxwTJ2YdtgqXfgaA+pScfrPok7cqutwVIaYvaVF/poRj8mYpLTDXHikGv1uHJ++tmnY+WD1O5nG4II8RFkVaQNRnYwRttP9SH6kQdB04t89/1O/w1cDnyilFU=','10fdf3d150416feab83aeb0f40957ba3','2025-12-27 22:45:23','2025-12-27 22:45:23'),(9,'GAE','總務工程','General Affairs & Engineering','Kh0qjTWkDHX3AsjwaflwFUh8QP9aEB62dbpKL1D2ExTv/zFdQyvWSrRIXlRSwn1WbEOcT0GQaN1Ec5LO1zCDR0WoG2IghuLvTPnPHPjd1E3ucEtoAS94dhjgtygroVhblhrKWoL9wOWkGuIaSEbaUgdB04t89/1O/w1cDnyilFU=','bc52327ede761af7bf6d69c84d993c79','2025-12-27 22:45:23','2025-12-27 22:45:23'),(10,'BB','飲料酒吧','Beverage & Bar','++yCqhlPe8PJCv2IPIzV9WNrvwM4YNYoTHgWakfo3OV9EtPhErAV448X4a+4iStkzNoWO9iL8DltrREPWq49OT4iim3w8Uh1M8ncbNpR5KTherDrlMMuEcQWiz7PpGO+4GCJG4hFAexJAZoz/ZgrJwdB04t89/1O/w1cDnyilFU=','79482b03a698feda10a0fdbff7665f78','2025-12-27 22:45:23','2025-12-27 22:45:23'),(11,'AD','美術設計','Art & Design','0+VkeT/tTERd640s5RhZTDFQC/Zsoe0xvmcGMko7js6BP8Z4ohpBHCHtC5iUs0swGvCiwlYfXW58FusubQ6YPTc+2nwOMiqgFk/mzKdTvlhHXviTQAudckmoGOBSbB77gEyKDhIht+PbKqVIKmIEsgdB04t89/1O/w1cDnyilFU=','dd0455de07c4d1653ba25a8a0b6f9631','2025-12-27 22:45:23','2025-12-27 22:45:23'),(12,'LA','休閒活動部','Leisure Activities','meO4TLMrgqT/uaM5fNTJcMkqhS52MeY+2+nkX1YJpcIAzsx2B/ANdOPE/XDWxj5/bvWGjiY6uaCiiHB0xCQEQOFX7t5NUSWBc/h9UAyJVZbpmr4K6L//PgavPFbgNIWM8walT8ZHPzSW8t0tsxwfYAdB04t89/1O/w1cDnyilFU=','024f57951d26aaceb7185834c1269766','2025-12-27 22:45:23','2025-12-27 22:45:23');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emotion_analysis`
--

DROP TABLE IF EXISTS `emotion_analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emotion_analysis` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '使用者 ID',
  `image_filename` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '影像檔案名稱',
  `image_data` blob COMMENT '影像二進位資料',
  `dominant_emotion` varchar(50) COLLATE utf8mb4_bin NOT NULL COMMENT '主要情緒: HAPPY, SAD, ANGRY, CONFUSED, DISGUSTED, SURPRISED, CALM, NEUTRAL',
  `dominant_emotion_confidence` float NOT NULL COMMENT '主要情緒信心度 (0-100)',
  `emotions_json` varchar(1000) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '所有情緒的信心度 (JSON格式)',
  `face_count` int DEFAULT NULL COMMENT '檢測到的臉部數量',
  `face_details_json` varchar(2000) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '臉部詳細資訊 (JSON)',
  `analysis_result_json` varchar(2000) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'AWS 完整分析結果 (JSON)',
  `status` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '分析狀態: success, processing, failed',
  `error_message` varchar(500) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '錯誤訊息 (若分析失敗)',
  `created_at` datetime DEFAULT (now()) COMMENT '建立時間',
  `updated_at` datetime DEFAULT (now()) COMMENT '更新時間',
  PRIMARY KEY (`id`),
  KEY `ix_emotion_analysis_id` (`id`),
  KEY `ix_emotion_analysis_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emotion_analysis`
--

LOCK TABLES `emotion_analysis` WRITE;
/*!40000 ALTER TABLE `emotion_analysis` DISABLE KEYS */;
/*!40000 ALTER TABLE `emotion_analysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emotional_tasks`
--

DROP TABLE IF EXISTS `emotional_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emotional_tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_code` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `task_id` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `dept_code` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `dept_name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `task_date` date DEFAULT NULL,
  `time_start` time DEFAULT NULL,
  `time_end` time DEFAULT NULL,
  `location_code` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `sequence_stage` varchar(5) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'P=準備 E=執行 F=收尾',
  `task_title` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `action_item` text COLLATE utf8mb4_bin,
  `note` text COLLATE utf8mb4_bin,
  `status` varchar(30) COLLATE utf8mb4_bin DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_emotional_task_id` (`task_id`),
  KEY `ix_emotional_tasks_dept_code` (`dept_code`),
  KEY `ix_emotional_tasks_id` (`id`),
  KEY `ix_emotional_tasks_status` (`status`),
  KEY `ix_emotional_tasks_task_date` (`task_date`),
  KEY `ix_emotional_tasks_project_code` (`project_code`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emotional_tasks`
--

LOCK TABLES `emotional_tasks` WRITE;
/*!40000 ALTER TABLE `emotional_tasks` DISABLE KEYS */;
INSERT INTO `emotional_tasks` VALUES (1,'VIC','VIC-AD-101','AD','美術設計部','2025-12-27','09:00:00','09:20:00','L01','P','品牌精神視覺','於大廳與會議廳架設「年度戰略」主題背板與歡迎布條。','結合客戶品牌色與運動元素。','completed','2025-12-27 14:50:46','2025-12-27 22:36:44','2025-12-27 22:50:46'),(2,'VIC','VIC-GAE-101','GAE','總務工程部','2025-12-27','09:25:00','09:45:00','B01','P','會議視聽巡檢','檢查國際會議廳 AV 設備、投影與 100 人份 Wi-Fi 負載。','確保簡報切換零延遲。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(3,'VIC','VIC-HK-101','HK','房務部','2025-12-27','09:50:00','10:10:00','S_ALL','P','舒緩備品設置','於客房內設置「足部放鬆貼布」與運動飲料。','呼應運動鞋產業久站/走特性。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(4,'VIC','VIC-FS-101','FS','花房','2025-12-27','10:15:00','10:35:00','B01','P','活力植栽佈置','會議桌佈置以「綠色植栽」為主，象徵永續與生機。','避免使用花粉過多花材。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(5,'VIC','VIC-BP-101','BP','烘焙點心房','2025-12-27','10:40:00','11:00:00','B01','E','能量補給茶點','準備高蛋白能量棒、全麥點心作為會議茶歇 (Coffee Break)。','配合運動員/健康形象。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(6,'VIC','VIC-GS-101','GS','客務部','2025-12-27','11:05:00','11:30:00','L01','P','團體快速入住','預製 100 份房卡套，執行「行動櫃台」分流辦理入住。','縮短主管等待時間。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(7,'VIC','VIC-CON-101','CON','門房諮詢服務中心','2025-12-27','11:35:00','12:00:00','L01','E','團體行李分送','依照部門別將行李掛牌分色，並直送客房。','確保會議結束後行李已在房內。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(8,'VIC','VIC-FB-101','F&B','餐飲部','2025-12-27','13:00:00','13:30:00','R01','E','戰鬥午餐服務','提供高效率自助餐 (Buffet)，設立現煮麵食區。','強調快速取餐與營養均衡。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(9,'VIC','VIC-LA-101','LA','休閒活動部','2025-12-27','14:00:00','14:30:00','B01','E','會議破冰活動','帶領 10 分鐘「辦公室伸展操」，提振下午會議精神。','簡單不流汗的動態活動。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(10,'VIC','VIC-LUR-101','LUR','洗衣房與制服室','2025-12-27','15:00:00','15:30:00','S_ALL','E','晚宴戰袍急件','收取主管需整燙的西裝/禮服，保證 18:00 前送回。','確保慶功宴儀容完美。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(11,'VIC','VIC-CBS-101','CBS','會議宴會部','2025-12-27','16:00:00','16:30:00','B01','P','場地翻場作業','將會議型態迅速轉換為「圓桌慶功晚宴」型態。','確認動線與舞台燈光。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(12,'VIC','VIC-BB-101','BB','飲料酒吧','2025-12-27','17:00:00','17:30:00','B01_Foyer','E','勝利特調接待','於宴會廳前廳提供以品牌色調製的 Welcome Cocktail。','包含無酒精選項。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(13,'VIC','VIC-FB-102','F&B','餐飲部','2025-12-27','18:00:00','18:30:00','B01','E','慶功晚宴開餐','執行 100 人同步上菜秀 (Synchronized Service)。','展現軍隊般的紀律與氣勢。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(14,'VIC','VIC-AD-102','AD','美術設計部','2025-12-27','19:00:00','19:30:00','B01','E','年度回顧投影','操作現場巨型螢幕，播放年度業績回顧與優秀員工表揚影片。','配合燈光音效。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(15,'VIC','VIC-LA-102','LA','休閒活動部','2025-12-27','20:00:00','20:30:00','B01','E','團隊凝聚遊戲','主持「部門對抗賽」或趣味競賽 (如綁鞋帶大賽)。','炒熱氣氛，增進跨部門情誼。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(16,'VIC','VIC-GAE-102','GAE','總務工程部','2025-12-27','21:00:00','21:30:00','B01','E','晚宴溫控監測','因飲酒與情緒高昂，適度調降空調溫度至 23 度。','保持空氣流通避免悶熱。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(17,'VIC','VIC-HK-102','HK','房務部','2025-12-27','21:40:00','22:00:00','S_ALL','P','深度開夜床','補充大量礦泉水於床頭，並放置解酒液或維他命 B 群。','貼心考量飲酒後的生理需求。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(18,'VIC','VIC-LA-201','LA','休閒活動部','2025-12-28','06:00:00','06:30:00','P01_Outside','E','CEO 晨跑領跑','規劃飯店周邊 5K 路線，由教練陪同 CEO 與主管晨跑。','需事前勘查路線安全性。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(19,'VIC','VIC-CON-201','CON','門房諮詢服務中心','2025-12-28','06:35:00','06:55:00','L01','E','跑者補給站','於大廳門口設置毛巾遞送與常溫水站。','迎接晨跑回來的貴賓。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(20,'VIC','VIC-BP-201','BP','烘焙點心房','2025-12-28','07:00:00','07:25:00','R01','F','健康香蕉吧','早餐區特別設置「香蕉與燕麥」專區 (運動員最愛)。','提供快速能量補充。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(21,'VIC','VIC-FB-201','F&B','餐飲部','2025-12-28','07:30:00','08:00:00','R01','F','活力早餐服務','早餐時段預留團體座位區，方便主管邊吃邊交流。','確保咖啡供應充足。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(22,'VIC','VIC-FS-201','FS','花房','2025-12-28','08:30:00','08:50:00','L01','F','獻花儀式準備','準備精緻花束，供離場前致贈給總經理與高階長官。','選用大氣的花材 (如鶴望蘭)。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(23,'VIC','VIC-CBS-201','CBS','會議宴會部','2025-12-28','09:00:00','09:30:00','B01','F','會場撤除檢查','檢查晚宴會場是否有遺留物 (如獎盃、私人物品)。','立即回報客務部。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(24,'VIC','VIC-BB-201','BB','飲料酒吧','2025-12-28','09:40:00','10:00:00','L01','F','離場外帶咖啡','於大廳準備 100 杯外帶熱美式/拿鐵 (To-go Cup)。','讓客人在回程車上享用。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(25,'VIC','VIC-LUR-201','LUR','洗衣房與制服室','2025-12-28','10:10:00','10:30:00','L01','F','遺留物確認','確認所有送洗的西裝/衣物皆已送回客房或交還客人。','零失誤檢查。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(26,'VIC','VIC-GS-201','GS','客務部','2025-12-28','10:40:00','11:00:00','L01','F','統一退房結帳','與財務長對接 Master Bill (總帳單)，主管免排隊直接退房。','確保帳目明細清晰。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(27,'VIC','VIC-GAE-201','GAE','總務工程部','2025-12-28','11:05:00','11:30:00','L01_Bus','F','遊覽車況檢視','協助司機檢查遊覽車冷氣與輪胎狀況 (安全第一)。','確保回程行車安全。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(28,'HLA','HLA-AD-101','AD','美術設計部','2025-12-27','10:00:00','10:20:00','S1205','P','迎賓文宣製作','製作「蜘蛛人入館任務卡」與「準爸媽週年賀卡」，放置於書桌顯眼處。','賀卡需包含對未來寶寶的祝福。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(29,'HLA','HLA-GAE-101','GAE','總務工程部','2025-12-27','10:25:00','10:45:00','S1205','F','客房安全巡檢','客房微氣候調整與安全巡檢，鎖定空調並檢查浴室。','空調鎖定恆溫 24-25°C；確認浴室防滑係數達標。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(30,'HLA','HLA-HK-101','HK','房務部','2025-12-27','10:50:00','11:10:00','S1205','P','雙主題房佈置','執行「雙重情境」佈置：大床玫瑰花瓣，小床蜘蛛人帳篷。','玫瑰花瓣避開枕頭睡眠區。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(31,'HLA','HLA-HK-102','HK','房務部','2025-12-27','11:15:00','11:35:00','S1205','P','孕幼備品設置','設置孕期與兒童專屬備品（S型抱枕、雙倍止滑墊）。','備品須為無香精、成份單純款式。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(32,'HLA','HLA-FS-101','FS','花房','2025-12-27','11:40:00','12:00:00','S1205','P','無粉花藝佈置','客房花藝佈置，選用淡雅色系鮮花。','嚴禁濃郁香氣（如百合），建議使用香檳玫瑰。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(33,'HLA','HLA-LUR-101','LUR','洗衣房與制服室','2025-12-27','12:05:00','12:30:00','K01','P','職人制服整燙','準備並熨燙「兒童職人體驗服裝」送至活動場地。','確認無殘留洗劑氣味。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(34,'HLA','HLA-CON-101','CON','門房諮詢服務中心','2025-12-27','14:00:00','14:15:00','L01','E','英雄式迎賓','接手行李與嬰兒車，以「超級英雄」稱號問候小朋友。','蹲下視線平行，告知有秘密任務。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(35,'HLA','HLA-GS-101','GS','客務部','2025-12-27','14:20:00','14:40:00','S1205','P','房內坐式入住','引導至房內沙發區辦理入住 (In-Room Check-in)。','系統備註「準媽媽」，同步全館。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(36,'HLA','HLA-BB-101','BB','飲料酒吧','2025-12-27','14:45:00','15:05:00','S1205','E','迎賓特調飲品','送達房內迎賓飲品：分層色果汁與熱蜂蜜檸檬水。','小孩飲品需呈現紅藍配色；媽媽飲品去冰溫熱。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(37,'HLA','HLA-BP-101','BP','烘焙點心房','2025-12-27','15:10:00','15:30:00','S1205','P','迎賓主題甜點','送達客房迎賓甜點：蜘蛛網餅乾與低糖燕麥點心。','媽媽點心需減糖低負擔。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(38,'HLA','HLA-LUR-102','LUR','洗衣房與制服室','2025-12-27','16:00:00','16:20:00','K01','P','小廚師著裝','協助小朋友更換合身的「小小廚師服」。','建立「專業廚師」自信心。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(39,'HLA','HLA-LA-101','LA','休閒活動部','2025-12-27','16:25:00','17:00:00','K01','E','小小廚師課程','執行「小小廚師」披薩/甜點製作課程。','教練稱呼孩子「超級英雄」；爸爸擔任助手。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(40,'HLA','HLA-CBS-101','CBS','會議宴會部','2025-12-27','17:05:00','17:15:00','K01','P','頒獎會場佈置','將教室一角佈置為「偽頒獎典禮」現場（紅地毯/背板）。','營造正式榮耀感。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(41,'HLA','HLA-LA-102','LA','休閒活動部','2025-12-27','17:15:00','17:30:00','K01','F','榮耀頒獎儀式','舉行頒獎儀式，頒發證書金牌並合影。','將遊戲轉化為學習歷程。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(42,'HLA','HLA-FS-102','FS','花房','2025-12-27','18:00:00','18:20:00','R01','E','晚宴花瓣佈置','於餐廳窗邊座位灑上新鮮玫瑰花瓣。','篩選淡香品種，營造視覺衝擊。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(43,'HLA','HLA-AD-102','AD','美術設計部','2025-12-27','18:25:00','18:40:00','R01','F','紀念菜單呈遞','呈遞專屬設計「結婚週年紀念菜單」。','菜單剔除生食、酒精等禁忌食材。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(44,'HLA','HLA-FB-101','F&B','餐飲部','2025-12-27','18:45:00','19:00:00','R01','E','貼心入座服務','引導入座，放置靠墊並展示蜘蛛人造型餐巾。','主動支撐孕婦腰部。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(45,'HLA','HLA-BB-102','BB','飲料酒吧','2025-12-27','19:05:00','19:20:00','R01','F','偽香檳乾杯','執行「偽裝香檳」乾杯服務 (Sparkling Juice)。','外觀需與真香檳一致。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(46,'HLA','HLA-BP-102','BP','烘焙點心房','2025-12-27','19:25:00','19:40:00','R01','E','手作驚喜上菜','將孩子手作甜點擺盤後作為驚喜前菜上桌。','提升孩子自我效能感。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(47,'HLA','HLA-FB-102','F&B','餐飲部','2025-12-27','19:45:00','20:10:00','R01','E','眾星拱月祝福','團隊獻花，配合燈光微調營造微煙火效果。','營造眾星拱月尊榮感。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(48,'HLA','HLA-AD-103','AD','美術設計部','2025-12-27','20:15:00','20:30:00','R01','F','紀念相框致贈','將合影修圖輸出，裝入紀念相框送達餐桌。','於結帳前送上即時驚喜。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(49,'HLA','HLA-GAE-102','GAE','總務工程部','2025-12-27','21:00:00','21:20:00','S1205','F','夜間照明巡檢','夜間照明巡檢，確認感應燈動線。','重點：床邊至廁所路徑。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(50,'HLA','HLA-HK-103','HK','房務部','2025-12-27','21:25:00','21:40:00','S1205','P','極致開夜床','開夜床服務，更換腳踏墊並補充溫開水。','確保浴室腳踏墊乾爽防滑。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(51,'HLA','HLA-FB-201','F&B','餐飲部','2025-12-28','08:00:00','08:30:00','S1205','F','孕期營養早餐','提供孕期營養建議早餐（熱湯、高蛋白）。','送餐時關懷睡眠狀況。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(52,'HLA','HLA-LA-201','LA','休閒活動部','2025-12-28','08:40:00','09:20:00','P01','F','池畔暖心服務','泳池畔預留防滑躺椅，提供毛毯與溫水。','確保媽媽舒適觀看。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(53,'HLA','HLA-CBS-201','CBS','會議宴會部','2025-12-28','09:30:00','09:50:00','L01','E','公區座椅更換','若客人在公區停留，主動更換支撐性好座椅。','避免孕婦坐姿不適。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(54,'HLA','HLA-CON-201','CON','門房諮詢服務中心','2025-12-28','10:30:00','10:50:00','L01','P','離場無縫送別','確認車輛冷氣預開，門口直接稱名道別。','省去報房號的生疏感。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44'),(55,'HLA','HLA-GS-201','GS','客務部','2025-12-28','11:00:00','11:30:00','L01','P','隱形結帳送客','隱形結帳，管家與小孩擊掌約定下次任務。','完成童趣送客。','pending',NULL,'2025-12-27 22:36:44','2025-12-27 22:36:44');
/*!40000 ALTER TABLE `emotional_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_reports`
--

DROP TABLE IF EXISTS `task_reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` varchar(50) COLLATE utf8mb4_bin NOT NULL COMMENT '任務編號',
  `step` int NOT NULL COMMENT '回報步驟',
  `answer` text COLLATE utf8mb4_bin COMMENT '回報內容',
  `created_at` datetime DEFAULT (now()) COMMENT '建立時間',
  PRIMARY KEY (`id`),
  KEY `ix_task_reports_id` (`id`),
  KEY `ix_task_reports_task_id` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_reports`
--

LOCK TABLES `task_reports` WRITE;
/*!40000 ALTER TABLE `task_reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '內部流水號',
  `task_uid` varchar(50) NOT NULL COMMENT '任務編號 (格式: YYYYMMDD-TYPE-TIMESTAMP)',
  `title` varchar(255) NOT NULL COMMENT '任務標題/事件簡述',
  `description` text COMMENT '任務詳細描述',
  `location` varchar(100) DEFAULT NULL COMMENT '發生地點 (如: 205 房, 大廳酒吧)',
  `department` varchar(50) DEFAULT NULL COMMENT '負責部門 (如: housekeeping, mis, fb)',
  `assignee_id` int DEFAULT NULL COMMENT '被指派人員ID (關聯 users.id)',
  `reporter_id` int DEFAULT NULL COMMENT '通報人員ID (關聯 users.id)',
  `priority` varchar(20) DEFAULT 'Medium' COMMENT '優先順序: Low, Medium, High, Critical',
  `is_emergency` tinyint(1) DEFAULT '0' COMMENT '是否為緊急事件 (0:否, 1:是)',
  `status` varchar(20) DEFAULT 'Pending' COMMENT '狀態: Pending(待派工), Dispatched(已派工), Processing(處理中), Completed(已完成), Cancelled(已取消)',
  `line_sent` tinyint(1) DEFAULT '0' COMMENT '是否已發送 Line 通知 (0:否, 1:是)',
  `line_message_id` varchar(100) DEFAULT NULL COMMENT 'Line 訊息 ID (用於追蹤或收回)',
  `line_sent_at` datetime DEFAULT NULL COMMENT 'Line 發送時間',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '建立時間',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新時間',
  `completed_at` datetime DEFAULT NULL COMMENT '實際完成時間',
  `due_at` datetime DEFAULT NULL COMMENT '預計完成期限',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_task_uid` (`task_uid`),
  KEY `idx_department` (`department`),
  KEY `idx_status` (`status`),
  KEY `idx_assignee` (`assignee_id`),
  KEY `idx_created_at` (`created_at`),
  KEY `fk_tasks_reporter` (`reporter_id`),
  CONSTRAINT `fk_tasks_assignee` FOREIGN KEY (`assignee_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_tasks_reporter` FOREIGN KEY (`reporter_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='派工任務資料表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,'20251219-FALL-1734570000','跌倒偵測','客人於浴室滑倒，請立即前往協助','205 浴室','housekeeping',NULL,NULL,'Critical',1,'Pending',0,NULL,NULL,'2025-12-19 01:00:34','2025-12-19 01:13:55',NULL,NULL),(2,'20251219-EMOT-1734571800','情緒激動','偵測到爭吵聲，請保安人員前往查看','大廳酒吧','security',NULL,NULL,'High',1,'Processing',0,NULL,NULL,'2025-12-19 00:30:34','2025-12-19 01:15:55',NULL,NULL),(3,'20251219-SERV-1734573600','呼叫服務','客人請求協助更換備品','302 客房','housekeeping',NULL,NULL,'Medium',0,'Pending',0,NULL,NULL,'2025-12-19 00:00:34','2025-12-19 01:00:34',NULL,NULL),(4,'20251219-NOIS-1734577200','噪音投訴','隔壁房客喧嘩，影響安寧','101 客房','front_office',NULL,NULL,'High',0,'Dispatched',0,NULL,NULL,'2025-12-18 23:00:34','2025-12-19 01:00:34',NULL,NULL),(5,'20251219-INJU-1734584400','意外受傷','泳池邊滑倒擦傷，需要急救箱','1F 戶外泳池','recreation',NULL,NULL,'Critical',1,'Completed',0,NULL,NULL,'2025-12-18 21:00:34','2025-12-19 01:00:34',NULL,NULL),(6,'20251219-CLEAN-001','客房清潔請求','VIP 客人要求立即清潔房間','501 總統套房','housekeeping',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 02:42:14','2025-12-19 02:52:14',NULL,NULL),(7,'20251219-SUPP-002','補充備品','客人需要額外的毛巾和洗漱用品','305 客房','housekeeping',NULL,NULL,'Low',0,'Completed',0,NULL,NULL,'2025-12-19 00:52:14','2025-12-19 02:52:14',NULL,NULL),(8,'20251219-LOST-003','遺失物協尋','客人表示找不到鑽石耳環，請求協助尋找','208 客房','housekeeping',NULL,NULL,'High',0,'Processing',0,NULL,NULL,'2025-12-19 02:07:14','2025-12-19 02:52:14',NULL,NULL),(9,'20251219-SPILL-004','走道清潔','3樓走廊有飲料打翻，需立即清理','3F 走廊','housekeeping',NULL,NULL,'Medium',0,'Dispatched',0,NULL,NULL,'2025-12-19 02:37:14','2025-12-19 02:52:14',NULL,NULL),(10,'20251219-AC-005','冷氣故障','客人反映冷氣不冷，室溫過高','402 客房','engineering',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 01:52:14','2025-12-19 02:52:14',NULL,NULL),(11,'20251219-LEAK-006','浴室漏水','洗手台下方水管漏水，地板積水','606 客房','engineering',NULL,NULL,'Critical',1,'Processing',0,NULL,NULL,'2025-12-19 02:22:14','2025-12-19 02:52:14',NULL,NULL),(12,'20251219-WIFI-007','網路連線異常','會議室 Wi-Fi 訊號不穩，無法視訊會議','2F 會議室 A','engineering',NULL,NULL,'High',0,'Dispatched',0,NULL,NULL,'2025-12-19 02:32:14','2025-12-19 02:52:14',NULL,NULL),(13,'20251219-LIFT-008','電梯異音','客用電梯 B 運作時有異常聲響','電梯 B','engineering',NULL,NULL,'Critical',1,'Pending',0,NULL,NULL,'2025-12-19 02:47:14','2025-12-19 02:52:14',NULL,NULL),(14,'20251219-LIGHT-009','燈泡更換','床頭閱讀燈閃爍','310 客房','engineering',NULL,NULL,'Low',0,'Completed',0,NULL,NULL,'2025-12-18 21:52:14','2025-12-19 02:52:14',NULL,NULL),(15,'20251219-FOOD-010','送餐延遲','客人投訴客房服務送餐超過 40 分鐘','505 客房','fb',NULL,NULL,'Medium',0,'Processing',0,NULL,NULL,'2025-12-19 02:42:14','2025-12-19 02:52:14',NULL,NULL),(16,'20251219-SPILL-011','餐廳打破杯子','西餐廳有客人打破紅酒杯，需清潔並安撫','1F 西餐廳','fb',NULL,NULL,'Medium',0,'Completed',0,NULL,NULL,'2025-12-18 23:52:14','2025-12-19 02:52:14',NULL,NULL),(17,'20251219-ICE-012','製冰機故障','酒吧製冰機停止運作','1F 大廳酒吧','engineering',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 02:02:14','2025-12-19 02:52:14',NULL,NULL),(18,'20251219-NOISE-013','噪音投訴','隔壁房客開派對聲音過大','701 客房','front_office',NULL,NULL,'High',0,'Dispatched',0,NULL,NULL,'2025-12-19 01:52:14','2025-12-19 02:52:14',NULL,NULL),(19,'20251219-KEY-014','房卡失效','客人房卡無法感應開門','405 客房','front_office',NULL,NULL,'Medium',0,'Completed',0,NULL,NULL,'2025-12-18 22:52:14','2025-12-19 02:52:14',NULL,NULL),(20,'20251219-VIP-015','VIP 接待','重要貴賓王董事長預計 10 分鐘後抵達','大廳門口','front_office',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 02:47:14','2025-12-19 02:52:14',NULL,NULL),(21,'20251219-FIRE-016','火警警報','廚房偵測到煙霧反應','B1 中央廚房','security',NULL,NULL,'Critical',1,'Processing',0,NULL,NULL,'2025-12-19 02:50:14','2025-12-19 02:52:14',NULL,NULL),(22,'20251219-FIGHT-017','客人爭執','大廳有兩位客人口角，需安保介入','1F 大廳','security',NULL,NULL,'High',1,'Completed',0,NULL,NULL,'2025-12-18 20:52:14','2025-12-19 02:52:14',NULL,NULL),(23,'20251219-SICK-018','客人身體不適','宴會廳有客人暈倒，已叫救護車','2F 宴會廳','front_office',NULL,NULL,'Critical',1,'Completed',0,NULL,NULL,'2025-12-18 02:52:14','2025-12-19 02:52:14',NULL,NULL),(24,'20251219-POOL-019','泳池水質異常','泳池水質混濁，需檢測氯含量','戶外泳池','recreation',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 00:52:14','2025-12-19 02:52:14',NULL,NULL),(25,'20251219-GYM-020','器材損壞','跑步機 3 號履帶卡住','健身房','engineering',NULL,NULL,'Medium',0,'Dispatched',0,NULL,NULL,'2025-12-18 23:52:14','2025-12-19 02:52:14',NULL,NULL),(26,'20251219-POS-021','POS 機當機','禮品店結帳櫃檯 POS 無法連線','1F 禮品店','mis',NULL,NULL,'High',0,'Processing',0,NULL,NULL,'2025-12-19 02:37:14','2025-12-19 02:52:14',NULL,NULL),(27,'20251219-PRINTER-022','印表機卡紙','櫃台印表機無法列印發票','1F 櫃台','mis',NULL,NULL,'Medium',0,'Completed',0,NULL,NULL,'2025-12-18 02:52:14','2025-12-19 02:52:14',NULL,NULL),(28,'20251219-FLOWER-023','婚宴花藝補強','主桌花飾有部分凋謝需更換','2F 宴會廳 A','florist',NULL,NULL,'Medium',0,'Pending',0,NULL,NULL,'2025-12-19 02:22:14','2025-12-19 02:52:14',NULL,NULL),(29,'20251219-LAUNDRY-024','急件送洗','客人要求西裝 2 小時內洗好燙平','602 客房','laundry',NULL,NULL,'High',0,'Processing',0,NULL,NULL,'2025-12-19 01:52:14','2025-12-19 02:52:14',NULL,NULL),(30,'20251219-LUGGAGE-025','行李運送','團體客 20 件行李需送至房間','大廳 -> 8F','concierge',NULL,NULL,'Medium',0,'Dispatched',0,NULL,NULL,'2025-12-19 02:42:14','2025-12-19 02:52:14',NULL,NULL),(31,'20251219-TAXI-026','叫車服務','客人預約機場接送，司機未到','大廳門口','concierge',NULL,NULL,'High',0,'Processing',0,NULL,NULL,'2025-12-19 02:47:14','2025-12-19 02:52:14',NULL,NULL),(32,'20251219-SMELL-027','異味通報','走廊有燒焦味','5F 電梯口','security',NULL,NULL,'Critical',1,'Dispatched',0,NULL,NULL,'2025-12-19 02:51:14','2025-12-27 16:37:36',NULL,NULL),(33,'20251219-PEST-028','蟲害通報','客房內發現蟑螂','201 客房','housekeeping',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 02:32:14','2025-12-19 02:52:14',NULL,NULL),(34,'20251219-GLASS-029','玻璃破裂','強風吹落陽台玻璃','905 客房','engineering',NULL,NULL,'Critical',1,'Dispatched',0,NULL,NULL,'2025-12-19 02:12:14','2025-12-19 02:52:14',NULL,NULL),(35,'20251219-BABY-030','嬰兒床需求','客人臨時需要加嬰兒床','408 客房','housekeeping',NULL,NULL,'Medium',0,'Completed',0,NULL,NULL,'2025-12-18 21:52:14','2025-12-19 02:52:14',NULL,NULL);
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '使用者名稱',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '電子郵件',
  `full_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '全名',
  `hashed_password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '加密後的密碼',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '帳號是否啟用',
  `created_at` datetime DEFAULT (now()) COMMENT '建立時間',
  `updated_at` datetime DEFAULT (now()) COMMENT '更新時間',
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT 'user' COMMENT '使用者角色: admin, manager, user',
  `department` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '部門',
  `last_login` datetime DEFAULT NULL COMMENT '最後登入時間',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_username` (`username`),
  UNIQUE KEY `ix_users_email` (`email`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin@ace.com','系統管理員','$2b$12$SasOiTJHV0F90V37a7OVwOpKrEq/EPaPV.1yYrSymI28bN15iT2Ya',1,'2025-12-10 12:11:07','2025-12-27 22:50:27','admin','mis','2025-12-27 22:50:28');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_analysis`
--

DROP TABLE IF EXISTS `video_analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `video_analysis` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '使用者 ID',
  `video_filename` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '影片檔案名稱',
  `video_format` varchar(10) COLLATE utf8mb4_bin NOT NULL COMMENT '影片格式: mp4, wmv, etc',
  `duration_seconds` float DEFAULT NULL COMMENT '影片時長（秒）',
  `total_frames` int DEFAULT NULL COMMENT '總幀數',
  `fps` float DEFAULT NULL COMMENT '幀率',
  `overall_dominant_emotion` varchar(50) COLLATE utf8mb4_bin NOT NULL COMMENT '整體主要情緒',
  `overall_confidence` float NOT NULL COMMENT '整體信心度',
  `frame_by_frame_analysis` text COLLATE utf8mb4_bin COMMENT '逐幀分析結果 (JSON)',
  `emotion_timeline` text COLLATE utf8mb4_bin COMMENT '情緒時間線 (JSON)',
  `emotion_statistics` text COLLATE utf8mb4_bin COMMENT '情緒統計資訊 (JSON)',
  `detected_people_count` int DEFAULT NULL COMMENT '檢測到的人物數量',
  `facial_expressions_json` text COLLATE utf8mb4_bin COMMENT '面部表情詳細資訊 (JSON)',
  `transcription_json` text COLLATE utf8mb4_bin COMMENT '語音轉文字結果 (JSON)',
  `transcription_text` text COLLATE utf8mb4_bin COMMENT '對話文字內容',
  `transcription_confidence` float DEFAULT NULL COMMENT '轉錄信心度',
  `speaker_segments` text COLLATE utf8mb4_bin COMMENT '說話人分段結果 (JSON)',
  `speaker_count` int DEFAULT NULL COMMENT '檢測到的說話人數量',
  `status` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '分析狀態: processing, success, failed',
  `progress` float DEFAULT NULL COMMENT '分析進度 (0-100)',
  `error_message` varchar(500) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '錯誤訊息',
  `created_at` datetime DEFAULT (now()) COMMENT '建立時間',
  `completed_at` datetime DEFAULT NULL COMMENT '完成時間',
  `updated_at` datetime DEFAULT (now()) COMMENT '更新時間',
  PRIMARY KEY (`id`),
  KEY `ix_video_analysis_id` (`id`),
  KEY `ix_video_analysis_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_analysis`
--

LOCK TABLES `video_analysis` WRITE;
/*!40000 ALTER TABLE `video_analysis` DISABLE KEYS */;
/*!40000 ALTER TABLE `video_analysis` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-27 22:56:42
