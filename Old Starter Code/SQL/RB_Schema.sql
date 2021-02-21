use ripe_bananas;
-- DROP TABLE IF EXISTS ripe_bananas.streamingservices ; 
CREATE TABLE IF NOT EXISTS ripe_bananas.streamingservices (
  Service_ID INT(11) AUTO_INCREMENT,
  Service_Name VARCHAR(250),
  Service_Type VARCHAR(50),
  Service_Img VARCHAR(1000),
  Service_URL VARCHAR(100),
  Popular INT(10) DEFAULT 0,
  PRIMARY KEY (Service_ID));
   
-- DROP TABLE IF EXISTS ripe_bananas.serviceselection; 
CREATE TABLE IF NOT EXISTS ripe_bananas.serviceselection (
  SRV_Selection_ID INT(11) AUTO_INCREMENT,
  Title_Searched VARCHAR (2000),
  Select_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
  User_ID INT(10),
  Service_ID INT(50),
  PRIMARY KEY (SRV_Selection_ID));
 
-- DROP TABLE IF EXISTS ripe_bananas.user_frequency; 
CREATE TABLE ripe_bananas.user_frequency (
  Frequency_ID int NOT NULL AUTO_INCREMENT,
  Frequency_Name varchar(100) DEFAULT NULL,
  Frequency_Description varchar(4000) DEFAULT NULL,
  PRIMARY KEY (Frequency_ID)
);

-- DROP TABLE IF EXISTS ripe_bananas.user_profile; 
CREATE TABLE ripe_bananas.user_profile (
  User_ID int NOT NULL AUTO_INCREMENT,
  User_Name varchar(100) DEFAULT NULL,
  First_Name varchar(50) DEFAULT NULL,
  Last_Name varchar(50) DEFAULT NULL,
  Age int DEFAULT NULL,
  Gender varchar(6) DEFAULT NULL,
  Frequency_ID int DEFAULT NULL,
  Zip_Code int DEFAULT NULL,
  Audit VARCHAR(1000) NULL,
  Date_Created datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (User_ID)
);

-- DROP TABLE IF EXISTS ripe_bananas.user_profile_services; 
CREATE TABLE ripe_bananas.user_profile_services (
  User_ID int DEFAULT NULL,
  Service_ID int DEFAULT NULL
);