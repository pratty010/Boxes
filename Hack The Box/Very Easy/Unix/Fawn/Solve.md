# Write Up for Hack The Box box - [Fawn](https://app.hackthebox.com/starting-point?tier=0)

Part of Starting Point. Guided Box

> Pratyush Prakhar (5#1NC#4N) - 08/25/2023


### TASKS

1. What does the 3-letter acronym FTP stand for? - **File Transfer Protocol**

2. Which port does the FTP service listen on usually? - **21** -->  [nmap file](nmap/all.nmap)

3. What acronym is used for the secure version of FTP?- **sftp** 

4. What is the command we can use to send an ICMP echo request to test our connection to the target? - **ping**

5. From your scans, what version is FTP running on the target? - **vsftpd 3.0.3** --> [nmap file](nmap/main.nmap)

6. From your scans, what OS type is running on the target? - **Unix**

7. What is the command we need to run in order to display the 'ftp' client help menu? - **ftp -h** 

8. What is username that is used over FTP when you want to log in without having an account? --> **Anonymous**

9. What is the response code we get for the FTP message 'Login successful'? - **230** --> [ftp file](ftp/ftp.out)

10. There are a couple of commands we can use to list the files and directories available on the FTP server. One is dir. What is the other that is a common way to list files on a Linux system. - **ls**

11. What is the command used to download the file we found on the FTP server? - **get**

12.  Submit root flag - **035db21c881520061c53e0536e44f815** --> [flag file](ftp/flag.txt)
