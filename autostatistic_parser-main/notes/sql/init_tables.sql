CREATE TABLE `exclude_titles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `createdon` datetime NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `monitor_settings` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) NOT NULL,
  `release_year_run` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `min_sold_count` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `offer_settings` (
  `item_id` int(11) NOT NULL,
  `user_id` int(10) NOT NULL,
  `excluded` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`item_id`,`user_id`),
  KEY `excluded` (`excluded`)
);

CREATE TABLE `offers_cards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `alias` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `alias` (`alias`)
);

Create Table: CREATE TABLE `offers_duplicates` (
  `item_id` int(11) NOT NULL,
  `related_id` int(11) NOT NULL,
  PRIMARY KEY (`item_id`,`related_id`)
);

Create Table: CREATE TABLE `offers_list` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `url` text DEFAULT NULL,
  `offer_id` varchar(100) NOT NULL,
  `hash` varchar(100) NOT NULL,
  `brand` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `price` int(11) DEFAULT 0,
  `description` text DEFAULT NULL,
  `release_year` int(11) DEFAULT NULL,
  `run` int(11) DEFAULT NULL,
  `body` varchar(255) DEFAULT NULL,
  `color` varchar(255) DEFAULT NULL,
  `tax` int(11) DEFAULT NULL,
  `engine_volume` float DEFAULT NULL,
  `power` int(11) DEFAULT NULL,
  `engine_type` varchar(255) DEFAULT NULL,
  `transmission` varchar(255) DEFAULT NULL,
  `drive` varchar(255) DEFAULT NULL,
  `hand_drive` varchar(255) DEFAULT NULL,
  `condition` varchar(255) DEFAULT NULL,
  `owners` varchar(255) DEFAULT NULL,
  `possession_time` varchar(255) DEFAULT NULL,
  `pts` varchar(255) DEFAULT NULL,
  `customs` varchar(255) DEFAULT NULL,
  `guarantee` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `sale_time` text DEFAULT NULL,
  `seller_type` varchar(100) DEFAULT NULL,
  `configuration` varchar(100) DEFAULT NULL,
  `inspections_number` int(11) DEFAULT 0,
  `duplicated` tinyint(1) NOT NULL DEFAULT 0,
  `viewed` tinyint(1) DEFAULT 0,
  `report_pts` text DEFAULT NULL,
  `report_legal` text DEFAULT NULL,
  `report_pts_owners` text DEFAULT NULL,
  `report_dtp` text DEFAULT NULL,
  `report_autoru_offers` text DEFAULT NULL,
  `report_mileges_graph` text DEFAULT NULL,
  `report_history` text DEFAULT NULL,
  `report_comments` text DEFAULT NULL,
  `report_untrusted` text DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `createdon` datetime DEFAULT NULL,
  `checkedon` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `brand` (`brand`),
  KEY `model_brand` (`model`,`brand`),
  KEY `price` (`price`),
  KEY `title` (`title`),
  KEY `release_year` (`release_year`),
  KEY `run` (`run`),
  KEY `body` (`body`),
  KEY `color` (`color`),
  KEY `power` (`power`),
  KEY `engine_type` (`engine_type`),
  KEY `transmission` (`transmission`),
  KEY `drive` (`drive`),
  KEY `hand_drive` (`hand_drive`),
  KEY `status` (`status`),
  KEY `inspections_number` (`inspections_number`),
  KEY `duplicated` (`duplicated`),
  KEY `viewed` (`viewed`),
  KEY `region` (`region`),
  KEY `engine_volume` (`engine_volume`),
  KEY `engine_volume_engine_type` (`engine_volume`,`engine_type`),
  KEY `condition_index` (`condition`),
  KEY `owners` (`owners`),
  KEY `pts` (`pts`),
  KEY `customs` (`customs`),
  KEY `checkedon_region_duplicated` (`checkedon`,`region`,`duplicated`),
  KEY `seller_type` (`seller_type`),
  KEY `configuration` (`configuration`)
);

CREATE TABLE `offers_notes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text DEFAULT NULL,
  `transmission` varchar(255) DEFAULT NULL,
  `drive` varchar(255) DEFAULT NULL,
  `body` varchar(255) DEFAULT NULL,
  `engine_volume` float DEFAULT NULL,
  `power` int(11) DEFAULT NULL,
  `engine_type` varchar(255) DEFAULT NULL,
  `note` text DEFAULT NULL,
  `createdon` datetime DEFAULT NULL,
  `changedon` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `offers_tracking` (
  `item_id` int(11) NOT NULL,
  `checkedon` datetime NOT NULL,
  `price` int(11) DEFAULT 0,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`item_id`,`checkedon`)
);

CREATE TABLE `regions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `alias_auto_ru` varchar(255) DEFAULT NULL,
  `gids_auto_ru` text DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `saved_searches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `title` text NOT NULL,
  `description` text NOT NULL,
  `query` text NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `users` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `active` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `active` (`active`)
);
