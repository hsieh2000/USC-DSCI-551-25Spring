
-- #1
WITH balance_sum AS (SELECT CustomerID, sum(Balance) as Total_Balance FROM `accounts` GROUP BY CustomerID)
SELECT CustomerID 
FROM (SELECT *, DENSE_RANK() OVER(ORDER BY Total_Balance DESC) AS RankNum FROM balance_sum) AS rank_table 
WHERE RankNum = 1;
-- +------------+
-- | CustomerID |
-- +------------+
-- | C005       |
-- +------------+
-- 1 row in set (0.00 sec)

-- #2
select distinct concat(c.FirstName, " ", c.LastName) as Name 
from accounts as a 
natural join 
branches as b 
natural join 
customers as c 
where b.BranchName = 'Downtown';
-- +---------------+
-- | Name          |
-- +---------------+
-- | John Doe      |
-- | Bob Brown     |
-- | David Taylor  |
-- | Hannah Miller |
-- +---------------+
-- 4 rows in set (0.00 sec)

-- #3
select distinct e.FirstName Name from branches as b 
natural join employees as e 
where b.BranchName = 'Downtown' and e.JobTitle = 'Branch Manager';
-- +------+
-- | Name |
-- +------+
-- | Mark |
-- +------+
-- 1 row in set (0.01 sec)

-- #4
WITH customer_counts AS (select count(distinct CustomerID) CustomerNum, BranchID from accounts group by BranchID)
SELECT b.BranchName FROM 
(SELECT *, DENSE_RANK() OVER(ORDER BY CustomerNum DESC) AS RankNum FROM customer_counts) AS rank_table 
natural join branches as b 
WHERE RankNum = 1;
-- +------------+
-- | BranchName |
-- +------------+
-- | Downtown   |
-- | Uptown     |
-- +------------+
-- 2 rows in set (0.00 sec)

-- #5
select concat(e.FirstName, " ", e.LastName) as `Name`, e.JobTitle from employees as e 
left join (select * from branches) as b 
on b.ManagerID = e.EmployeeID 
where b.ManagerID IS NULL 
ORDER BY `Name`;

-- #6
-- set operation
select CustomerID from accounts where BranchID = 'B001' and AccountType = 'Savings' 
INTERSECT 
select CustomerID from accounts  where BranchID = 'B001' and AccountType = 'Checking';
-- +------------+
-- | CustomerID |
-- +------------+
-- | C001       |
-- +------------+
-- 1 row in set (0.00 sec)

-- join
SELECT distinct a.CustomerID FROM accounts a
NATURAL JOIN (SELECT CustomerID FROM accounts WHERE BranchID = 'B001' AND AccountType = 'Checking') AS b
WHERE a.BranchID = 'B001' AND a.AccountType = 'Savings';
-- +------------+
-- | CustomerID |
-- +------------+
-- | C001       |
-- +------------+
-- 1 row in set (0.00 sec)

-- subquery
SELECT DISTINCT a.CustomerID
FROM accounts a
WHERE a.BranchID = 'B001' AND a.AccountType = 'Savings'AND a.CustomerID IN (
SELECT CustomerID FROM accounts WHERE BranchID = 'B001' AND AccountType = 'Checking');
-- +------------+
-- | CustomerID |
-- +------------+
-- | C001       |
-- +------------+
-- 1 row in set (0.00 sec)

-- #7
SELECT b.BranchName
FROM branches b
LEFT JOIN (SELECT BranchID, COUNT(*) AS employee_count FROM employees GROUP BY BranchID HAVING employee_count >= 3) e 
ON b.BranchID = e.BranchID
WHERE e.BranchID is not NULL;
-- +------------+
-- | BranchName |
-- +------------+
-- | Suburbia   |
-- +------------+
-- 1 row in set (0.01 sec)
