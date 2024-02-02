# Write Up for Hack The Box box - [Vaccine](https://app.hackthebox.com/starting-point?tier=1)

Part of Starting Point. Very Easy, Guided Box

> Pratyush Prakhar (5#1NC#4N) - 09/09/2023


### TASKS

1. Besides SSH and HTTP, what other service is hosted on this box? - **FTP** --> [nmap file](nmap/main.nmap)

2. This service can be configured to allow login with any password for specific username. What is that username? - **Anonymous** --> [FTP out file](ftp/ftp.out)

3. What is the name of the file downloaded over this service? - **backup.zip**

4. What script comes with the John The Ripper toolset and generates a hash from a password protected zip archive in a format to allow for cracking attempts? - **zip2john** --> [zip hash file](ftp/backupziphash), [zip passwd](ftp/backup_cracked_hash), [backup folder](ftp/backup)

5. What is the password for the admin user on the website? - **qwerty789** --> [password file](web/admin_pass)

6. What option can be passed to sqlmap to try to get command execution via the sql injection? - **--os-shell** 

7. What program can the postgres user run as root using sudo? - **vi** 

8. Submit user flag - **ec9b13ca4d6229cd5cc1e09980965bf7** --> [user.txt file](ssh/var/lib/postgresql/user.txt)

9. Submit root flag - **dd6e058e814260bc70e9bbdef2715849** --> [root.txt file](ssh/root/root.txt)

