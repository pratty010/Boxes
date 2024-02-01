# Write Up for Hack The Box box - [Appointment](https://app.hackthebox.com/starting-point?tier=1)

Part of Starting Point Path. Guided Box

> Pratyush Prakhar (5#1NC#4N) - 08/25/2023


### TASKS

1. What does the acronym SQL stand for? - **Structured Query Language**

2. What is one of the most common type of SQL vulnerabilities? - **SQL Injection**

3. What is the 2021 OWASP Top 10 classification for this vulnerability? - **A03:2021-Injection**

4. What does Nmap report as the service and version that are running on port 80 of the target? - **Apache httpd 2.4.38** --> [nmap file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Appointment/nmap/main.nmap)

5. What is the standard port used for the HTTPS protocol?- **443**

6. What is a folder called in web-application terminology? - **directory**

7. What is the HTTP response code is given for 'Not Found' errors? - **404** 

8. Gobuster is one tool used to brute force directories on a webserver. What switch do we use with Gobuster to specify we're looking to discover directories, and not subdomains? - **dir**

9. What single character can be used to comment out the rest of a line in MySQL? - **#** --> [SQL File](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Appointment/web/sqldump.log)

10. If user input is not handled carefully, it could be interpreted as a comment. Use a comment to login as admin without knowing the password. What is the first word on the webpage returned? - **Congratulations!**

11. Submit root flag - **e3d0796d002a446c0e622226f42e9672**
![](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Appointment/images/flag.png)
