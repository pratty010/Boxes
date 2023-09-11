# Write Up for Hack The Box box - [Crocodile](https://app.hackthebox.com/starting-point?tier=1)

Part of Starting Point. Guided Box

> Pratyush Prakhar (5#1NC#4N) - 08/26/2023


### TASKS

1. What Nmap scanning switch employs the use of default scripts during a scan? - **-sC**

2. What service version is found to be running on port 21? - **vsftpd 3.0.3** --> [nmap file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Crocodile/nmap/main.nmap)

3. What FTP code is returned to us for the "Anonymous FTP login allowed" message? - **230**

4. After connecting to the FTP server using the ftp client, what username do we provide when prompted to log in anonymously? - **Anonymous**

5. After connecting to the FTP server anonymously, what command can we use to download the files we find on the FTP server? - **get**

6. What is one of the higher-privilege sounding usernames in 'allowed.userlist' that we download from the FTP server? - **admin** --> [user file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Crocodile/ftp/allowed.userlist)

7. What version of Apache HTTP Server is running on the target host? - **Apache httpd 2.4.41** --> [nmap file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Crocodile/nmap/main.nmap)

8. What switch can we use with Gobuster to specify we are looking for specific filetypes? --> **-x**

9. Which PHP file can we identify with directory brute force that will provide the opportunity to authenticate to the web service? - **login.php** --> [feroxbuster file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Crocodile/web/port_80.txt)

10. Submit root flag - **c7110277ac44d78b6a9fff2232434d16** 
![](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Crocodile/images/flag_dash.png)
