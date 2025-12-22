CREATE DATABASE  IF NOT EXISTS `ace` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ace`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 192.168.50.101    Database: ace
-- ------------------------------------------------------
-- Server version	9.5.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'c484ec14-cdbb-11f0-b837-22037a439215:1-443';

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '部門ID',
  `code` varchar(20) NOT NULL COMMENT '部門代碼 (簡寫)',
  `name_en` varchar(100) NOT NULL COMMENT '英文名稱',
  `name_zh` varchar(100) NOT NULL COMMENT '中文名稱',
  `channel_name` varchar(100) DEFAULT NULL COMMENT 'Line Channel 名稱',
  `channel_id` varchar(50) DEFAULT NULL COMMENT 'Line Channel ID',
  `bot_basic_id` varchar(50) DEFAULT NULL COMMENT 'Line Bot Basic ID (@xxx)',
  `channel_access_token` text COMMENT 'Line Channel Access Token',
  `channel_secret` varchar(100) DEFAULT NULL COMMENT 'Line Channel Secret',
  `qr_code_url` varchar(255) DEFAULT NULL COMMENT 'QR Code 圖片連結',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '建立時間',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新時間',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code` (`code`),
  UNIQUE KEY `uk_bot_basic_id` (`bot_basic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='部門與 Line Bot 設定資料表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'GS','Guest Services','客務部','GS 客務部','2008665810','@677anhlp','MxuOtBSYhdm1T0XMAHonGiiIyIlwzVQ+4sTxW25Grruzxlz3TC+q50mxkcmu9dnnqkq1e8RNKm0bKoGlQETCC1X0/JoIkhkBobcT4c1Mz97YyvTdGSYMFQnQC/EZ1xwZawymWJihprpaLteucQ6gqgdB04t89/1O/w1cDnyilFU=','ca87c1e2f974953a128e7dec4454f4fb',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(2,'HK','Housekeeping','房務部','HK 房務部','2008665366','@753flmfy','HpQnEQnQkHnJrjUqnDhCf6VjDUbpFo3vfcgQmoIYRodHh41xBqKi5veh0ng/Fpb83O/bwMb2cl3PectuRXnFhAxUAQ9pOXXImUbhMrsDtX/Ojc8sjut7p8tm62eF7p9PBJHm0cjlU+4XvpQlBiukcgdB04t89/1O/w1cDnyilFU=','6484246f951afec8dacd6d3ca1f5056b',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(3,'CON','Concierge','門房諮詢服務中心','CON門房諮詢服務中心','2008665961','@208woevo','GgrwJ9o5Ob96ylf70vUr7yM1iJuyAG7UPWCJ0J7hsCrOXxZbKwuXdWSOmBxnP1VPgmfeEDe4NvF3yZQNnGYSVx/Zz/n/1YL6hHUHOx6NzKe/23rXNJYH9Fg0yrSwNri9xhOA4PlZhQBqaqWo1rnnzQdB04t89/1O/w1cDnyilFU=','bec44c0da0920af55cd2af04650c767e',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(4,'BP','Bakery & Pastry','烘焙點心房','BP 烘焙點心房','2008666473','@783yclgw','p3IKt8qxi38bWa99f9zrFb7O1UNVioV2XspJTXcGOcDl5pGd6BvZiRb/ZiGYtpxweHz5IxaHdWHZ0+4YyBDK5UUTW6Nvr1js3jVa/AhvsODv66Gm17fq4r4PZh5U5FDZxeUesGiLuuXLNju5uTFkSwdB04t89/1O/w1cDnyilFU=','246b6237d02d448396b2d8f856827637',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(5,'FB','Food & Beverage','餐飲','FB 餐飲','2008666603','@617oqtwl','HLK6AtfByF+obzujnta/XxhT9QD1JeDqYwFjiQryYRwXvKZvW3joLfS12EjI4LDyhsUYQTMFdNWEB2ocOkylOgVtTcaOPf51oFXYWbL6/ri9AVfWqDGMeD5J5q2+TtHzNE092UdhaT35zk85Pp3d6QdB04t89/1O/w1cDnyilFU=','43019aef0ed7626c454e1a02795da0cc',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(6,'CBS','Conference & Banquet Services','會議宴會','CBS 會議宴會','2008666865','@939wzhrk','7iCPU+jjVueLE3GuWB/dBeJnocZD2ugA2S8vP82tocOqepa4wFWKr/jVww37EDk3Xhzr4OViyGYq0XvEpd8nexfpECEVBb0Iz5DQm+3KSex9rtQiNJ+GInCo2fisbsxcJ8wqIIAnvBJzPg5K+DU7kwdB04t89/1O/w1cDnyilFU=','1edff2612ed91a6821bcf393fee7ad97',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(7,'FS','Flower Shop','花房','FS 花房','2008666808','@864nopzp','QARjCy6uOvP55smmIUNiRSq0eTaUIfv3aQxvN6MZc0i/r+kTN1iAVDzpVi3irWWP1bIpeAGhQex8z9PKV133bSsWOYEjdu6QSJtqX+H0afzmoNfcD+Lyg2TVE1PmJCwVduZly9gvSIQOsQ5fPMPtuQdB04t89/1O/w1cDnyilFU=','1f99fae43459eb6eb1e8a58cb6ac1c96',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(8,'LUR','Laundry & Uniform Room','洗衣房與制服室','LUR 洗衣房與制服室','2008666883','@184yvbia','UwAvvI1P0oGbX+WaWFTVtVOWUVzEd99cVMuMSxkkvrY5/poKBxmxwTJ2YdtgqXfgaA+pScfrPok7cqutwVIaYvaVF/poRj8mYpLTDXHikGv1uHJ++tmnY+WD1O5nG4II8RFkVaQNRnYwRttP9SH6kQdB04t89/1O/w1cDnyilFU=','10fdf3d150416feab83aeb0f40957ba3',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(9,'GAE','General Affairs & Engineering','總務工程','GAE 總務工程','2008666975','@022bxdyn','Kh0qjTWkDHX3AsjwaflwFUh8QP9aEB62dbpKL1D2ExTv/zFdQyvWSrRIXlRSwn1WbEOcT0GQaN1Ec5LO1zCDR0WoG2IghuLvTPnPHPjd1E3ucEtoAS94dhjgtygroVhblhrKWoL9wOWkGuIaSEbaUgdB04t89/1O/w1cDnyilFU=','bc52327ede761af7bf6d69c84d993c79',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(10,'BB','Beverage & Bar','飲料酒吧','BB 飲料酒吧','2008666845','@736fanmi','++yCqhlPe8PJCv2IPIzV9WNrvwM4YNYoTHgWakfo3OV9EtPhErAV448X4a+4iStkzNoWO9iL8DltrREPWq49OT4iim3w8Uh1M8ncbNpR5KTherDrlMMuEcQWiz7PpGO+4GCJG4hFAexJAZoz/ZgrJwdB04t89/1O/w1cDnyilFU=','79482b03a698feda10a0fdbff7665f78',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(11,'AD','Art & Design','美術設計','AD 美術設計','2008667002','@148zhfpe','0+VkeT/tTERd640s5RhZTDFQC/Zsoe0xvmcGMko7js6BP8Z4ohpBHCHtC5iUs0swGvCiwlYfXW58FusubQ6YPTc+2nwOMiqgFk/mzKdTvlhHXviTQAudckmoGOBSbB77gEyKDhIht+PbKqVIKmIEsgdB04t89/1O/w1cDnyilFU=','dd0455de07c4d1653ba25a8a0b6f9631',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28'),(12,'LA','Leisure Activities','休閒活動部','LA 休閒活動部','2008667024','@404eknsv','meO4TLMrgqT/uaM5fNTJcMkqhS52MeY+2+nkX1YJpcIAzsx2B/ANdOPE/XDWxj5/bvWGjiY6uaCiiHB0xCQEQOFX7t5NUSWBc/h9UAyJVZbpmr4K6L//PgavPFbgNIWM8walT8ZHPzSW8t0tsxwfYAdB04t89/1O/w1cDnyilFU=','024f57951d26aaceb7185834c1269766',NULL,'2025-12-19 01:42:28','2025-12-19 01:42:28');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='派工任務資料表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,'20251219-FALL-1734570000','跌倒偵測','客人於浴室滑倒，請立即前往協助','205 浴室','housekeeping',NULL,NULL,'Critical',1,'Pending',0,NULL,NULL,'2025-12-19 01:00:34','2025-12-19 01:13:55',NULL,NULL),(2,'20251219-EMOT-1734571800','情緒激動','偵測到爭吵聲，請保安人員前往查看','大廳酒吧','security',NULL,NULL,'High',1,'Processing',0,NULL,NULL,'2025-12-19 00:30:34','2025-12-19 01:15:55',NULL,NULL),(3,'20251219-SERV-1734573600','呼叫服務','客人請求協助更換備品','302 客房','housekeeping',NULL,NULL,'Medium',0,'Pending',0,NULL,NULL,'2025-12-19 00:00:34','2025-12-19 01:00:34',NULL,NULL),(4,'20251219-NOIS-1734577200','噪音投訴','隔壁房客喧嘩，影響安寧','101 客房','front_office',NULL,NULL,'High',0,'Dispatched',0,NULL,NULL,'2025-12-18 23:00:34','2025-12-19 01:00:34',NULL,NULL),(5,'20251219-INJU-1734584400','意外受傷','泳池邊滑倒擦傷，需要急救箱','1F 戶外泳池','recreation',NULL,NULL,'Critical',1,'Completed',0,NULL,NULL,'2025-12-18 21:00:34','2025-12-19 01:00:34',NULL,NULL),(6,'20251219-CLEAN-001','客房清潔請求','VIP 客人要求立即清潔房間','501 總統套房','housekeeping',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 02:42:14','2025-12-19 02:52:14',NULL,NULL),(7,'20251219-SUPP-002','補充備品','客人需要額外的毛巾和洗漱用品','305 客房','housekeeping',NULL,NULL,'Low',0,'Completed',0,NULL,NULL,'2025-12-19 00:52:14','2025-12-19 02:52:14',NULL,NULL),(8,'20251219-LOST-003','遺失物協尋','客人表示找不到鑽石耳環，請求協助尋找','208 客房','housekeeping',NULL,NULL,'High',0,'Processing',0,NULL,NULL,'2025-12-19 02:07:14','2025-12-19 02:52:14',NULL,NULL),(9,'20251219-SPILL-004','走道清潔','3樓走廊有飲料打翻，需立即清理','3F 走廊','housekeeping',NULL,NULL,'Medium',0,'Dispatched',0,NULL,NULL,'2025-12-19 02:37:14','2025-12-19 02:52:14',NULL,NULL),(10,'20251219-AC-005','冷氣故障','客人反映冷氣不冷，室溫過高','402 客房','engineering',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 01:52:14','2025-12-19 02:52:14',NULL,NULL),(11,'20251219-LEAK-006','浴室漏水','洗手台下方水管漏水，地板積水','606 客房','engineering',NULL,NULL,'Critical',1,'Processing',0,NULL,NULL,'2025-12-19 02:22:14','2025-12-19 02:52:14',NULL,NULL),(12,'20251219-WIFI-007','網路連線異常','會議室 Wi-Fi 訊號不穩，無法視訊會議','2F 會議室 A','engineering',NULL,NULL,'High',0,'Dispatched',0,NULL,NULL,'2025-12-19 02:32:14','2025-12-19 02:52:14',NULL,NULL),(13,'20251219-LIFT-008','電梯異音','客用電梯 B 運作時有異常聲響','電梯 B','engineering',NULL,NULL,'Critical',1,'Pending',0,NULL,NULL,'2025-12-19 02:47:14','2025-12-19 02:52:14',NULL,NULL),(14,'20251219-LIGHT-009','燈泡更換','床頭閱讀燈閃爍','310 客房','engineering',NULL,NULL,'Low',0,'Completed',0,NULL,NULL,'2025-12-18 21:52:14','2025-12-19 02:52:14',NULL,NULL),(15,'20251219-FOOD-010','送餐延遲','客人投訴客房服務送餐超過 40 分鐘','505 客房','fb',NULL,NULL,'Medium',0,'Processing',0,NULL,NULL,'2025-12-19 02:42:14','2025-12-19 02:52:14',NULL,NULL),(16,'20251219-SPILL-011','餐廳打破杯子','西餐廳有客人打破紅酒杯，需清潔並安撫','1F 西餐廳','fb',NULL,NULL,'Medium',0,'Completed',0,NULL,NULL,'2025-12-18 23:52:14','2025-12-19 02:52:14',NULL,NULL),(17,'20251219-ICE-012','製冰機故障','酒吧製冰機停止運作','1F 大廳酒吧','engineering',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 02:02:14','2025-12-19 02:52:14',NULL,NULL),(18,'20251219-NOISE-013','噪音投訴','隔壁房客開派對聲音過大','701 客房','front_office',NULL,NULL,'High',0,'Dispatched',0,NULL,NULL,'2025-12-19 01:52:14','2025-12-19 02:52:14',NULL,NULL),(19,'20251219-KEY-014','房卡失效','客人房卡無法感應開門','405 客房','front_office',NULL,NULL,'Medium',0,'Completed',0,NULL,NULL,'2025-12-18 22:52:14','2025-12-19 02:52:14',NULL,NULL),(20,'20251219-VIP-015','VIP 接待','重要貴賓王董事長預計 10 分鐘後抵達','大廳門口','front_office',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 02:47:14','2025-12-19 02:52:14',NULL,NULL),(21,'20251219-FIRE-016','火警警報','廚房偵測到煙霧反應','B1 中央廚房','security',NULL,NULL,'Critical',1,'Processing',0,NULL,NULL,'2025-12-19 02:50:14','2025-12-19 02:52:14',NULL,NULL),(22,'20251219-FIGHT-017','客人爭執','大廳有兩位客人口角，需安保介入','1F 大廳','security',NULL,NULL,'High',1,'Completed',0,NULL,NULL,'2025-12-18 20:52:14','2025-12-19 02:52:14',NULL,NULL),(23,'20251219-SICK-018','客人身體不適','宴會廳有客人暈倒，已叫救護車','2F 宴會廳','front_office',NULL,NULL,'Critical',1,'Completed',0,NULL,NULL,'2025-12-18 02:52:14','2025-12-19 02:52:14',NULL,NULL),(24,'20251219-POOL-019','泳池水質異常','泳池水質混濁，需檢測氯含量','戶外泳池','recreation',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 00:52:14','2025-12-19 02:52:14',NULL,NULL),(25,'20251219-GYM-020','器材損壞','跑步機 3 號履帶卡住','健身房','engineering',NULL,NULL,'Medium',0,'Dispatched',0,NULL,NULL,'2025-12-18 23:52:14','2025-12-19 02:52:14',NULL,NULL),(26,'20251219-POS-021','POS 機當機','禮品店結帳櫃檯 POS 無法連線','1F 禮品店','mis',NULL,NULL,'High',0,'Processing',0,NULL,NULL,'2025-12-19 02:37:14','2025-12-19 02:52:14',NULL,NULL),(27,'20251219-PRINTER-022','印表機卡紙','櫃台印表機無法列印發票','1F 櫃台','mis',NULL,NULL,'Medium',0,'Completed',0,NULL,NULL,'2025-12-18 02:52:14','2025-12-19 02:52:14',NULL,NULL),(28,'20251219-FLOWER-023','婚宴花藝補強','主桌花飾有部分凋謝需更換','2F 宴會廳 A','florist',NULL,NULL,'Medium',0,'Pending',0,NULL,NULL,'2025-12-19 02:22:14','2025-12-19 02:52:14',NULL,NULL),(29,'20251219-LAUNDRY-024','急件送洗','客人要求西裝 2 小時內洗好燙平','602 客房','laundry',NULL,NULL,'High',0,'Processing',0,NULL,NULL,'2025-12-19 01:52:14','2025-12-19 02:52:14',NULL,NULL),(30,'20251219-LUGGAGE-025','行李運送','團體客 20 件行李需送至房間','大廳 -> 8F','concierge',NULL,NULL,'Medium',0,'Dispatched',0,NULL,NULL,'2025-12-19 02:42:14','2025-12-19 02:52:14',NULL,NULL),(31,'20251219-TAXI-026','叫車服務','客人預約機場接送，司機未到','大廳門口','concierge',NULL,NULL,'High',0,'Processing',0,NULL,NULL,'2025-12-19 02:47:14','2025-12-19 02:52:14',NULL,NULL),(32,'20251219-SMELL-027','異味通報','走廊有燒焦味','5F 電梯口','security',NULL,NULL,'Critical',1,'Pending',0,NULL,NULL,'2025-12-19 02:51:14','2025-12-19 02:52:14',NULL,NULL),(33,'20251219-PEST-028','蟲害通報','客房內發現蟑螂','201 客房','housekeeping',NULL,NULL,'High',0,'Pending',0,NULL,NULL,'2025-12-19 02:32:14','2025-12-19 02:52:14',NULL,NULL),(34,'20251219-GLASS-029','玻璃破裂','強風吹落陽台玻璃','905 客房','engineering',NULL,NULL,'Critical',1,'Dispatched',0,NULL,NULL,'2025-12-19 02:12:14','2025-12-19 02:52:14',NULL,NULL),(35,'20251219-BABY-030','嬰兒床需求','客人臨時需要加嬰兒床','408 客房','housekeeping',NULL,NULL,'Medium',0,'Completed',0,NULL,NULL,'2025-12-18 21:52:14','2025-12-19 02:52:14',NULL,NULL);
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
  `username` varchar(50) COLLATE utf8mb4_bin NOT NULL COMMENT '使用者名稱',
  `email` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '電子郵件',
  `full_name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '全名',
  `hashed_password` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '加密後的密碼',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '帳號是否啟用',
  `created_at` datetime DEFAULT (now()) COMMENT '建立時間',
  `updated_at` datetime DEFAULT (now()) COMMENT '更新時間',
  `role` varchar(20) COLLATE utf8mb4_bin DEFAULT 'user' COMMENT '使用者角色: admin, manager, user',
  `department` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '部門',
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
INSERT INTO `users` VALUES (1,'admin','admin@ace.com','系統管理員','$2b$12$SasOiTJHV0F90V37a7OVwOpKrEq/EPaPV.1yYrSymI28bN15iT2Ya',1,'2025-12-10 12:11:07','2025-12-19 02:42:51','admin','mis','2025-12-19 02:42:52');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'ace'
--

--
-- Dumping routines for database 'ace'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-19  2:56:41
