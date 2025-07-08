SET @old_autocommit=@@autocommit;
CREATE DATABASE `banking` DEFAULT CHARACTER SET utf8mb4;
USE `banking`;

DROP TABLE IF EXISTS `branches`;
CREATE TABLE `branches` (
    `BranchID` char(4) NOT NULL DEFAULT '',
    `BranchName` varchar(64) NOT NULL DEFAULT '',
    `BranchAddress` varchar(255) NOT NULL DEFAULT '',
    `ManagerID` char(4) NOT NULL DEFAULT '',
    PRIMARY KEY (`BranchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

set autocommit=0;
-- insert data
INSERT INTO `branches` VALUES ('B001','Downtown','100 Downtown St, City', 'E001');
INSERT INTO `branches` VALUES ('B002','Uptown','200 Uptown Ave, Town', 'E002');
INSERT INTO `branches` VALUES ('B003','Suburbia','300 Suburb St, Suburbia', 'E003');
INSERT INTO `branches` VALUES ('B004','Eastside','400 East St, City', 'E006');
INSERT INTO `branches` VALUES ('B005','Westside','500 West St, Town', 'E007');
commit;

DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
    `CustomerID` char(4) NOT NULL DEFAULT '',
    `FirstName` varchar(64) NOT NULL DEFAULT '',
    `LastName` varchar(64) NOT NULL DEFAULT '',
    `Email` varchar(255) NOT NULL DEFAULT '',
    `PhoneNumber` char(12) NOT NULL DEFAULT '',
    `Address` varchar(255) NOT NULL DEFAULT '',
    PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

set autocommit=0;
-- insert data
INSERT INTO `customers` VALUES ('C001', 'John', 'Doe', 'john.doe@email.com', '123-456-7890', '123 Main St, City, USA');
INSERT INTO `customers` VALUES ('C002', 'Jane', 'Smith', 'jane.smith@email.com', '987-654-3210', '456 Oak Rd, Town, USA');
INSERT INTO `customers` VALUES ('C003', 'Alice', 'Johnson', 'alice.johnson@email.com', '555-123-4567', '789 Pine St, Suburbia, USA');
INSERT INTO `customers` VALUES ('C004', 'Bob', 'Brown', 'bob.brown@email.com', '444-987-6543', '101 Maple Ave, City, USA');
INSERT INTO `customers` VALUES ('C005', 'Carol', 'White', 'carol.white@email.com', '333-567-8901', '202 Birch Blvd, Town, USA');
INSERT INTO `customers` VALUES ('C006', 'David', 'Taylor', 'david.taylor@email.com', '222-333-4444', '303 Cedar St, City, USA');
INSERT INTO `customers` VALUES ('C007', 'Eve', 'Wilson', 'eve.wilson@email.com', '555-666-7777', '404 Elm St, Town, USA');
INSERT INTO `customers` VALUES ('C008', 'Frank', 'Davis', 'frank.davis@email.com', '888-999-0000', '505 Maple Ave, Suburbia, USA');
INSERT INTO `customers` VALUES ('C009', 'Grace', 'Lopez', 'grace.lopez@email.com', '123-321-4321', '606 Oak Blvd, City, USA');
INSERT INTO `customers` VALUES ('C010', 'Hannah', 'Miller', 'hannah.miller@email.com', '654-321-9876', '707 Pine Rd, Town, USA');
commit;

DROP TABLE IF EXISTS `employees`;
CREATE TABLE `employees` (
    `EmployeeID` char(4) NOT NULL DEFAULT '',
    `FirstName` varchar(64) NOT NULL DEFAULT '',
    `LastName` varchar(64) NOT NULL DEFAULT '',
    `JobTitle` varchar(255) NOT NULL DEFAULT '',
    `Salary` int NOT NULL DEFAULT 0,
    `BranchID` char(4) NOT NULL DEFAULT '',
    PRIMARY KEY (`EmployeeID`),
    KEY `BranchID` (`BranchID`),
    CONSTRAINT `fk_employees_branches` FOREIGN KEY (`BranchID`) REFERENCES `branches` (`BranchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

set autocommit=0;
-- insert data
INSERT INTO `employees` VALUES ('E001','Mark','Johnson', 'Branch Manager', 5000, 'B001');
INSERT INTO `employees` VALUES ('E002','Sarah','Davis', 'Branch Manager', 3000,'B002');
INSERT INTO `employees` VALUES ('E003','James','Clark', 'Branch Manager', 5500,'B003');
INSERT INTO `employees` VALUES ('E004','Emma','Wilson', 'Teller', 2900,'B003');
INSERT INTO `employees` VALUES ('E005','David','Lee', 'Teller', 3100,'B001');
INSERT INTO `employees` VALUES ('E006','Isabella','Martinez', 'Branch Manager', 5200,'B004');
INSERT INTO `employees` VALUES ('E007','Jacob','Taylor', 'Branch Manager', 3200,'B005');
INSERT INTO `employees` VALUES ('E008','Mason','Jackson', 'Teller', 3300,'B004');
INSERT INTO `employees` VALUES ('E009','Liam','Miller', 'Teller', 5700,'B005');
INSERT INTO `employees` VALUES ('E010','Olivia','Garcia', 'Teller', 3000,'B003');
commit;

DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
    `AccountID` char(4) NOT NULL DEFAULT '',
    `CustomerID` char(4) NOT NULL DEFAULT '',
    `AccountType` varchar(64) NOT NULL DEFAULT '',
    `Balance` float NOT NULL DEFAULT 0.0,
    `BranchID` char(4) NOT NULL DEFAULT '',
    PRIMARY KEY (`AccountID`),
    -- KEY `CustomerID`(`CustomerID`),
    -- KEY `BranchID`(`BranchID`),
    CONSTRAINT `fk_accounts_customers` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`),
    CONSTRAINT `fk_accounts_branches` FOREIGN KEY (`BranchID`) REFERENCES `branches` (`BranchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

set autocommit=0;
-- insert data
insert into `accounts` VALUES('A001', 'C001', 'Savings', '1500.0', 'B001');
insert into `accounts` VALUES('A002', 'C002', 'Checking', '2000.0', 'B002');
insert into `accounts` VALUES('A003', 'C001', 'Checking', '500.0', 'B001');
insert into `accounts` VALUES('A004', 'C003', 'Savings', '3000.0', 'B003');
insert into `accounts` VALUES('A005', 'C004', 'Checking', '2500.0', 'B001');
insert into `accounts` VALUES('A006', 'C005', 'Savings', '7000.0', 'B002');
insert into `accounts` VALUES('A007', 'C005', 'Checking', '4000.0', 'B003');
insert into `accounts` VALUES('A008', 'C006', 'Savings', '1000.0', 'B001');
insert into `accounts` VALUES('A009', 'C007', 'Checking', '2500.0', 'B002');
insert into `accounts` VALUES('A010', 'C008', 'Savings', '4500.0', 'B003');
insert into `accounts` VALUES('A011', 'C009', 'Checking', '6000.0', 'B002');
insert into `accounts` VALUES('A012', 'C010', 'Savings', '3500.0', 'B001');
commit;

SET autocommit=@old_autocommit;
