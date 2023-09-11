# Write Up for Hack The Box box - [Sequel](https://app.hackthebox.com/starting-point?tier=1)

Part of Starting Point. Very Easy, Guided Box

> Pratyush Prakhar (5#1NC#4N) - 08/26/2023


### TASKS

1. During our scan, which port do we find serving MySQL? - **3306** --> [nmap file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Sequel/nmap/all.nmap)

2. What community-developed MySQL version is the target running? - **MariaDB** --> [nmap file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Sequel/nmap/main.nmap)

3. When using the MySQL command line client, what switch do we need to use in order to specify a login username? - **-u**

4. Which username allows us to log into this MariaDB instance without providing a password? - **root**

5. In SQL, what symbol can we use to specify within the query that we want to display everything inside a table? - __*__

6. In SQL, what symbol do we need to end each query with? - **;** 

7. There are three databases in this MySQL instance that are common across all MySQL instances. What is the name of the fourth that's unique to this host? - **htb** --> [sql file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Sequel/mysql/db.md)

8. Submit root flag - **7b4bec00d1a39e3dd4e021ec3d915da8** 

