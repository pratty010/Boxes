# Write Up for Hack The Box box - [Sequel](https://app.hackthebox.com/starting-point?tier=1)

Part of Starting Point. Very Easy, Guided Box

> Pratyush Prakhar (5#1NC#4N) - 08/26/2023


### TASKS

1. During our scan, which port do we find serving MySQL? - **3306** --> [nmap file]()

2. What community-developed MySQL version is the target running? - **MariaDB** --> [nmap file]()

3. When using the MySQL command line client, what switch do we need to use in order to specify a login username? - **-u**

4. Which username allows us to log into this MariaDB instance without providing a password? - **root**

5. In SQL, what symbol can we use to specify within the query that we want to display everything inside a table? - __*__

6. In SQL, what symbol do we need to end each query with? - **;** 

7. There are three databases in this MySQL instance that are common across all MySQL instances. What is the name of the fourth that's unique to this host? - **htb** --> [sql file]()

8. What switch can we use with Gobuster to specify we are looking for specific filetypes? --> **-x**

9. Which PHP file can we identify with directory brute force that will provide the opportunity to authenticate to the web service? - **login.php** --> [feroxbuster file]()

10. Submit root flag - **7b4bec00d1a39e3dd4e021ec3d915da8** 

