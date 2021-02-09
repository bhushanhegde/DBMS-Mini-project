#Back end code to create table using SQL
#Use these codes to create tables.
'''
#SQL Table Creation

mysql> CREATE DATABASE farmer_app;
Query OK, 1 row affected (0.44 sec)

mysql> USE farmer_app;
Database changed
mysql> CREATE TABLE farmer(
    -> f_id INT,
    -> f_name VARCHAR(20),
    -> f_phone_no VARCHAR(11),
    -> f_mail VARCHAR(20),
    -> f_locality VARCHAR(20),
    -> f_address VARCHAR(30),
    -> PRIMARY KEY (f_id));
Query OK, 0 rows affected (1.53 sec)

mysql> CREATE TABLE company(
    -> c_id INT,
    -> c_name VARCHAR(20),
    -> c_address VARCHAR(30),
    -> PRIMARY KEY (c_id));
Query OK, 0 rows affected (1.37 sec)

mysql> CREATE TABLE fertilizer(
    -> fe_formula VARCHAR(20),
    -> fe_name VARCHAR(20),
    -> fe_content VARCHAR(30),
    -> fe_price INT,
    -> company_id INT,
    -> PRIMARY KEY (fe_formula),
    -> FOREIGN KEY (company_id) REFERENCES company(c_id));
Query OK, 0 rows affected (2.29 sec)

mysql> CREATE TABLE order(
    -> o_id INT,
    -> o_date DATETIME,
    -> o_farmer_id INT,
    -> o_formula VARCHAR(20),
    -> o_to VARCHAR(20),
    -> PRIMARY KEY (o_id),
    -> FOREIGN KEY (o_farmer_id) REFERENCES farmer(f_id),
    -> FOREIGN KEY (o_formula) REFERENCES fertilizer(fe_formula));
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'order(
o_id INT,
o_date DATETIME,
o_farmer_id INT,
o_formula VARCHAR(20),
o_to V' at line 1

mysql> CREATE TABLE payment(
    -> trans_id INT,
    -> p_f_id INT,
    -> p_date DATETIME,
    -> p_amount INT,
    -> p_method VARCHAR(20),
    -> PRIMARY KEY (trans_id),
    -> FOREIGN KEY (p_f_id) REFERENCES farmer(f_id));
Query OK, 0 rows affected (1.93 sec)

mysql> mysql> CREATE TABLE orders(
    ->      or_id INT,
    ->      or_date DATETIME,
    ->     or_fid INT,
    ->      or_formula VARCHAR(20),
    ->      or_to VARCHAR(20),
    ->      PRIMARY KEY (or_id),
    ->      FOREIGN KEY (or_fid) REFERENCES farmer(f_id),
    ->      FOREIGN KEY (or_formula) REFERENCES fertilizer(fe_formula));
Query OK, 0 rows affected (1.76 sec)

mysql> show tables;
+----------------------+
| Tables_in_farmer_app |
+----------------------+
| company              |
| farmer               |
| fertilizer           |
| orders               |
| payment              |
+----------------------+
5 rows in set (0.00 sec)

mysql>
ysql> USE farmer_app;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+----------------------+
| Tables_in_farmer_app |
+----------------------+
| company              |
| farmer               |
| fertilizer           |
| orders               |
| payment              |
+----------------------+
5 rows in set (0.00 sec)

mysql> describe company;
+-----------+-------------+------+-----+---------+-------+
| Field     | Type        | Null | Key | Default | Extra |
+-----------+-------------+------+-----+---------+-------+
| c_id      | int         | NO   | PRI | NULL    |       |
| c_name    | varchar(20) | YES  |     | NULL    |       |
| c_address | varchar(30) | YES  |     | NULL    |       |
+-----------+-------------+------+-----+---------+-------+
3 rows in set (0.00 sec)

mysql> describe farmer;
+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| f_id       | int         | NO   | PRI | NULL    |       |
| f_name     | varchar(20) | YES  |     | NULL    |       |
| f_phone_no | varchar(11) | YES  |     | NULL    |       |
| f_mail     | varchar(20) | YES  |     | NULL    |       |
| f_locality | varchar(20) | YES  |     | NULL    |       |
| f_address  | varchar(30) | YES  |     | NULL    |       |
+------------+-------------+------+-----+---------+-------+
6 rows in set (0.01 sec)

mysql> describe fertilizer;
+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| fe_formula | varchar(20) | NO   | PRI | NULL    |       |
| fe_name    | varchar(20) | YES  |     | NULL    |       |
| fe_content | varchar(30) | YES  |     | NULL    |       |
| fe_price   | int         | YES  |     | NULL    |       |
| company_id | int         | YES  | MUL | NULL    |       |
+------------+-------------+------+-----+---------+-------+
5 rows in set (0.00 sec)

mysql> describe order;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'order' at line 1
mysql> describe orders;
+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| or_id      | int         | NO   | PRI | NULL    |       |
| or_date    | datetime    | YES  |     | NULL    |       |
| or_fid     | int         | YES  | MUL | NULL    |       |
| or_formula | varchar(20) | YES  | MUL | NULL    |       |
| or_to      | varchar(20) | YES  |     | NULL    |       |
+------------+-------------+------+-----+---------+-------+
5 rows in set (0.01 sec)

mysql> describe payment;
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| trans_id | int         | NO   | PRI | NULL    |       |
| p_f_id   | int         | YES  | MUL | NULL    |       |
| p_date   | datetime    | YES  |     | NULL    |       |
| p_amount | int         | YES  |     | NULL    |       |
| p_method | varchar(20) | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+
5 rows in set (0.00 sec)

mysql>

'''
