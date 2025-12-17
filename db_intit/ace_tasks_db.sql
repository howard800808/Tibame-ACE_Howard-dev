CREATE DATABASE  IF NOT EXISTS `tibame_ace_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tibame_ace_db`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: tibame_ace_db
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
-- Table structure for table `hotel_tasks`
--

DROP TABLE IF EXISTS `hotel_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotel_tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `task_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `day` int NOT NULL,
  `time_start` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `time_end` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dept_code` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dept_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location_code` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sequence` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `action_item` text COLLATE utf8mb4_unicode_ci,
  `note` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `guest_adults` int DEFAULT NULL,
  `guest_children` int DEFAULT NULL,
  `guest_room_id` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `guest_special_needs` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT (now()),
  `updated_at` timestamp NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_hotel_tasks_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel_tasks`
--

LOCK TABLES `hotel_tasks` WRITE;
/*!40000 ALTER TABLE `hotel_tasks` DISABLE KEYS */;
INSERT INTO `hotel_tasks` VALUES (29,'Hero_Love_Anniversary_Project','AD-D1P-01','迎賓文宣製作',1,'10:00','10:20','AD','美術設計部','S1205','P','製作「蜘蛛人入館任務卡」與「準爸媽週年賀卡」，放置於書桌顯眼處。','賀卡需包含對未來寶寶的祝福。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:05','2025-12-17 03:36:35'),(30,'Hero_Love_Anniversary_Project','GAE-D1F-01','客房安全巡檢',1,'10:25','10:45','GAE','總務工程部','S1205','F','客房微氣候調整與安全巡檢，鎖定空調並檢查浴室。','空調鎖定恆溫 24-25°C；確認浴室防滑係數達標。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:05','2025-12-17 00:57:05'),(31,'Hero_Love_Anniversary_Project','HK-D1P-01','雙主題房佈置',1,'10:50','11:10','HK','房務部','S1205','P','執行「雙重情境」佈置：大床玫瑰花瓣，小床蜘蛛人帳篷。','玫瑰花瓣避開枕頭睡眠區。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:05','2025-12-17 00:57:05'),(32,'Hero_Love_Anniversary_Project','HK-D1P-02','孕幼備品設置',1,'11:15','11:35','HK','房務部','S1205','P','設置孕期與兒童專屬備品（S型抱枕、雙倍止滑墊）。','備品須為無香精、成份單純款式。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:05','2025-12-17 00:57:05'),(33,'Hero_Love_Anniversary_Project','FS-D1P-01','無粉花藝佈置',1,'11:40','12:00','FS','花房','S1205','P','客房花藝佈置，選用淡雅色系鮮花。','嚴禁濃郁香氣（如百合），建議使用香檳玫瑰。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:05','2025-12-17 00:57:05'),(34,'Hero_Love_Anniversary_Project','LUR-D1P-01','職人制服整燙',1,'12:05','12:30','LUR','洗衣房與制服室','K01','P','準備並熨燙「兒童職人體驗服裝」送至活動場地。','確認無殘留洗劑氣味。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:05','2025-12-17 00:57:05'),(35,'Hero_Love_Anniversary_Project','CON-D1E-01','英雄式迎賓',1,'14:00','14:15','CON','門房諮詢服務中心','L01','E','接手行李與嬰兒車，以「超級英雄」稱號問候小朋友。','蹲下視線平行，告知有秘密任務。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:05','2025-12-17 00:57:05'),(36,'Hero_Love_Anniversary_Project','GS-D1P-01','房內坐式入住',1,'14:20','14:40','GS','客務部','S1205','P','引導至房內沙發區辦理入住 (In-Room Check-in)。','系統備註「準媽媽」，同步全館。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:05','2025-12-17 00:57:05'),(37,'Hero_Love_Anniversary_Project','BB-D1E-01','迎賓特調飲品',1,'14:45','15:05','BB','飲料酒吧','S1205','E','送達房內迎賓飲品：分層色果汁與熱蜂蜜檸檬水。','小孩飲品需呈現紅藍配色；媽媽飲品去冰溫熱。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(38,'Hero_Love_Anniversary_Project','BP-D1P-01','迎賓主題甜點',1,'15:10','15:30','BP','烘焙點心房','S1205','P','送達客房迎賓甜點：蜘蛛網餅乾與低糖燕麥點心。','媽媽點心需減糖低負擔。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(39,'Hero_Love_Anniversary_Project','LUR-D1P-02','小廚師著裝',1,'16:00','16:20','LUR','洗衣房與制服室','K01','P','協助小朋友更換合身的「小小廚師服」。','建立「專業廚師」自信心。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(40,'Hero_Love_Anniversary_Project','LA-D1E-01','小小廚師課程',1,'16:25','17:00','LA','休閒活動部','K01','E','執行「小小廚師」披薩/甜點製作課程。','教練稱呼孩子「超級英雄」；爸爸擔任助手。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(41,'Hero_Love_Anniversary_Project','CBS-D1P-01','頒獎會場佈置',1,'17:05','17:15','CBS','會議宴會部','K01','P','將教室一角佈置為「偽頒獎典禮」現場（紅地毯/背板）。','營造正式榮耀感。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(42,'Hero_Love_Anniversary_Project','LA-D1F-02','榮耀頒獎儀式',1,'17:15','17:30','LA','休閒活動部','K01','F','舉行頒獎儀式，頒發證書金牌並合影。','將遊戲轉化為學習歷程。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(43,'Hero_Love_Anniversary_Project','FS-D1E-02','晚宴花瓣佈置',1,'18:00','18:20','FS','花房','R01','E','於餐廳窗邊座位灑上新鮮玫瑰花瓣。','篩選淡香品種，營造視覺衝擊。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(44,'Hero_Love_Anniversary_Project','AD-D1F-02','紀念菜單呈遞',1,'18:25','18:40','AD','美術設計部','R01','F','呈遞專屬設計「結婚週年紀念菜單」。','菜單剔除生食、酒精等禁忌食材。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(45,'Hero_Love_Anniversary_Project','FB-D1E-01','貼心入座服務',1,'18:45','19:00','FB','餐飲部','R01','E','引導入座，放置靠墊並展示蜘蛛人造型餐巾。','主動支撐孕婦腰部。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(46,'Hero_Love_Anniversary_Project','BB-D1F-02','偽香檳乾杯',1,'19:05','19:20','BB','飲料酒吧','R01','F','執行「偽裝香檳」乾杯服務 (Sparkling Juice)。','外觀需與真香檳一致。\n[01:45] LINEBot accept\n[01:45] LINEBot complete','done',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 01:45:51'),(47,'Hero_Love_Anniversary_Project','BP-D1E-02','手作驚喜上菜',1,'19:25','19:40','BP','烘焙點心房','R01','E','將孩子手作甜點擺盤後作為驚喜前菜上桌。','提升孩子自我效能感。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(48,'Hero_Love_Anniversary_Project','FB-D1E-02','眾星拱月祝福',1,'19:45','20:10','FB','餐飲部','R01','E','團隊獻花，配合燈光微調營造微煙火效果。','營造眾星拱月尊榮感。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(49,'Hero_Love_Anniversary_Project','AD-D1F-03','紀念相框致贈',1,'20:15','20:30','AD','美術設計部','R01','F','將合影修圖輸出，裝入紀念相框送達餐桌。','於結帳前送上即時驚喜。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(50,'Hero_Love_Anniversary_Project','GAE-D1F-02','夜間照明巡檢',1,'21:00','21:20','GAE','總務工程部','S1205','F','夜間照明巡檢，確認感應燈動線。','重點：床邊至廁所路徑。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(51,'Hero_Love_Anniversary_Project','HK-D1P-03','極致開夜床',1,'21:25','21:40','HK','房務部','S1205','P','開夜床服務，更換腳踏墊並補充溫開水。','確保浴室腳踏墊乾爽防滑。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(52,'Hero_Love_Anniversary_Project','FB-D2F-01','孕期營養早餐',2,'08:00','08:30','FB','餐飲部','S1205','F','提供孕期營養建議早餐（熱湯、高蛋白）。','送餐時關懷睡眠狀況。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(53,'Hero_Love_Anniversary_Project','LA-D2F-01','池畔暖心服務',2,'08:40','09:20','LA','休閒活動部','P01','F','泳池畔預留防滑躺椅，提供毛毯與溫水。','確保媽媽舒適觀看。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(54,'Hero_Love_Anniversary_Project','CBS-D2E-01','公區座椅更換',2,'09:30','09:50','CBS','會議宴會部','L01','E','若客人在公區停留，主動更換支撐性好座椅。','避免孕婦坐姿不適。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(55,'Hero_Love_Anniversary_Project','CON-D2P-01','離場無縫送別',2,'10:30','10:50','CON','門房諮詢服務中心','L01','P','確認車輛冷氣預開，門口直接稱名道別。','省去報房號的生疏感。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06'),(56,'Hero_Love_Anniversary_Project','GS-D2P-01','隱形結帳送客',2,'11:00','11:30','GS','客務部','L01','P','隱形結帳，管家與小孩擊掌約定下次任務。','完成童趣送客。','pending',2,1,'S1205','[\"Pregnancy_6M\", \"Anniversary\", \"Spiderman_Fan\"]','2025-12-17 00:57:06','2025-12-17 00:57:06');
/*!40000 ALTER TABLE `hotel_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_reports`
--

DROP TABLE IF EXISTS `task_reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `step` int NOT NULL,
  `answer` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_task_reports_id` (`id`),
  KEY `ix_task_reports_task_id` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_reports`
--

LOCK TABLES `task_reports` WRITE;
/*!40000 ALTER TABLE `task_reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_reports` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-17 12:45:13
