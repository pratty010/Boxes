# Writeup for the Try_Hack_Me box - Kenobi. 

The box utilizes **Samba share** for enumeration and get on the box. <ADD details about the privesc>
 
> Pratyush Prakhar (5#1NC#4N) - 08/11/2023

# RECON

1. Scan the machine with nmap, how many ports are open? - **7**

```bash
nmap -vv -sC -sV -oN nmap/main 10.10.224.128
```
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

# FTP

1. FTP is a basic file transfer protocol which allows to host a part of file system for access. 
2. For access, one might need `credentials` for acess. This provides a part for `fuzzing attacks` but might be caught by access logging mechanisms ont he system. Thus, a risk to follow this attack path. 
3. In this case, we have the `ProFTPD 1.3.5` which has password protection.
4. Let's look into any exploit that might be possible using `searchsploit` 
   1. Both `mod_copy` exploit fail due to non-writable paths.
5. Let's move on to next options. We can use it once we have some credentials.

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

# SSH

1. The system has OpenSSH installed which requires login by a valid user on the allowlist.,
2. We can fuzz with tools like `hydra` and `wfuzz` but is a high resistance task. 
3. We can get foothold with a set of valid credentials.


# SMB

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


# NFS
 <Working on it>


**Stay Tuned On**\
[Github](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)
