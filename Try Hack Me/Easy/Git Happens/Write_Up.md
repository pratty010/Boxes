# Write Up for Try Hack Me box - [Git Happens](https://tryhackme.com/room/githappens)

This box is based on a vulnerable git directory exposed.
We can use that to determine earlier changes and possible secrets. Let's jump in.

> Pratyush Prakhar (5#1NC#4N) - 09/09/2023


## RECONNAISSANCE

1. Scan the box with rustscan.

**Results**

```bash
# Nmap 7.94 scan initiated Thu Oct 26 07:26:00 2023 as: nmap -vvv -p 80 -sC -sV -oN nmap/main.nmap 10.10.252.173
Nmap scan report for 10.10.252.173
Host is up, received syn-ack (0.20s latency).
Scanned at 2023-10-26 07:26:01 EDT for 11s

PORT   STATE SERVICE REASON  VERSION
80/tcp open  http    syn-ack nginx 1.14.0 (Ubuntu)
| http-git: 
|   10.10.252.173:80/.git/
|     Git repository found!
|_    Repository description: Unnamed repository; edit this file 'description' to name the...
|_http-server-header: nginx/1.14.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-title: Super Awesome Site!
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

2. Following **TCP ports** are open. 
	1. *Port 80* - HTTP - **nginx 1.14.0**

3. Let's look into it.

![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Git%20Happens/images/web.png)


## WEB

1. We start with a typical check directory brute-force scan. We find that there is a `.git` directory that is leaked for the static webpage. Let's look into methods to exploit it. The full [FeroxBuster scan](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Git%20Happens/web/ferox.txt) file is here for reference.

**Results**

```bash
$ feroxbuster -vv -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt -u http://10.10.252.173 -x txt,sh,html,txt -o ferox.txt 
301      GET        7l       13w      194c http://10.10.252.173/css => http://10.10.252.173/css/
200      GET      199l      375w     5603c http://10.10.252.173/css/style.css
200      GET       60l      153w     6890c http://10.10.252.173/
MSG      0.000 feroxbuster::heuristics detected directory listing: http://10.10.252.173/css (Apache)
200      GET       60l      153w     6890c http://10.10.252.173/index.html
200      GET       16l       78w     3775c http://10.10.252.173/dashboard.html
301      GET        7l       13w      194c http://10.10.252.173/css => http://10.10.252.173/css/
.........................................................................................................
MSG      0.000 feroxbuster::heuristics detected directory listing: http://10.10.252.173/.git/info (Apache)
MSG      0.000 feroxbuster::heuristics detected directory listing: http://10.10.252.173/.git/hooks (Apache)
MSG      0.000 feroxbuster::heuristics detected directory listing: http://10.10.252.173/.git/refs (Apache)
MSG      0.000 feroxbuster::heuristics detected directory listing: http://10.10.252.173/.git/branches (Apache)
MSG      0.000 feroxbuster::heuristics detected directory listing: http://10.10.252.173/.git/logs (Apache)
MSG      0.000 feroxbuster::heuristics detected directory listing: http://10.10.252.173/.git/objects (Apache)
200      GET        6l       43w      240c http://10.10.252.173/.git/info/exclude
200      GET       24l      163w      896c http://10.10.252.173/.git/hooks/commit-msg.sample
200      GET        8l       32w      189c http://10.10.252.173/.git/hooks/post-update.sample
200      GET      169l      798w     4898c http://10.10.252.173/.git/hooks/pre-rebase.sample
200      GET       14l       69w      424c http://10.10.252.173/.git/hooks/pre-applypatch.sample
200      GET       24l       83w      544c http://10.10.252.173/.git/hooks/pre-receive.sample
200      GET       49l      275w     1642c http://10.10.252.173/.git/hooks/pre-commit.sample
200      GET       53l      230w     1348c http://10.10.252.173/.git/hooks/pre-push.sample
200      GET       15l       79w      478c http://10.10.252.173/.git/hooks/applypatch-msg.sample
200      GET      128l      539w     3610c http://10.10.252.173/.git/hooks/update.sample
200      GET      114l      513w     3327c http://10.10.252.173/.git/hooks/fsmonitor-watchman.sample
200      GET       42l      238w     1492c http://10.10.252.173/.git/hooks/prepare-commit-msg.sample
200      GET        1l        9w      216c http://10.10.252.173/.git/logs/HEAD
...............................................................................................................
```

2. [Nikto scan](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Git%20Happens/web/nikto.out) also confirms the same.

**Results**

```bash
$ nikto -url http://10.10.252.173/ -output nikto.out
- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.10.227.105
+ Target Hostname:    10.10.227.105
+ Target Port:        80
+ Start Time:         2023-09-10 22:02:23 (GMT-4)
---------------------------------------------------------------------------
+ Server: nginx/1.14.0 (Ubuntu)
+ Server leaks inodes via ETags, header found with file /, fields: 0x5f1a11a7 0x1aea 
+ The anti-clickjacking X-Frame-Options header is not present.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ OSVDB-3092: /.git/index: Git Index file may contain directory listing information.
+ 6544 items checked: 0 error(s) and 3 item(s) reported on remote host
+ End Time:           2023-09-10 22:26:22 (GMT-4) (1439 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

3. We can also confirm it on the web server as `http://10.10.252.173/.git/`. Let's explore this path.

![](https://github.com/pratty010/Boxes/blob/master/Try%20Hack%20Me/Easy/Git%20Happens/images/git.png)


## GIT

1. Git is a distributed version control system that tracks changes in any set of computer files, usually used for coordinating work among programmers who are collaboratively developing source code during software development. Its goals include speed, data integrity, and support for distributed, non-linear workflows. If you have never interacted with git, you are still in Stone Age. But I got you covered. Look here when you get the internet in 5000 years or so --> https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F

2. Now as we have figured that out, let's jump into the some juicy enumeration. One of the great places to checkout is the mecca called [HackTricks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/git).
   1. The common path is to get dump all the available git material to local.
   2. Now we can explore all the material to find any hidden information. This includes web resources, backend services, etc.
   3. Other places to checkout are logs, history, past commits, etc.

3. I am going to use the world famous [Git Tools](https://github.com/internetwache/GitTools) to dump the .git repo data. 

4. Using the `git log` command we get all the past commits which are not cleaned. We find that there is a conversation about obfuscating and encryption of the data. This is where we can find some shared secrets that might exist in plaintext form. Let's check each commit.

```bash
$ git log                                          
commit d0b3578a628889f38c0affb1b75457146a4678e5 (HEAD -> master, tag: v1.0)
Author: Adam Bertrand <hydragyrum@gmail.com>
Date:   Thu Jul 23 22:22:16 2020 +0000

    Update .gitlab-ci.yml

commit 77aab78e2624ec9400f9ed3f43a6f0c942eeb82d
Author: Hydragyrum <hydragyrum@gmail.com>
Date:   Fri Jul 24 00:21:25 2020 +0200

    add gitlab-ci config to build docker file.

commit 2eb93ac3534155069a8ef59cb25b9c1971d5d199
Author: Hydragyrum <hydragyrum@gmail.com>
Date:   Fri Jul 24 00:08:38 2020 +0200

    setup dockerfile and setup defaults.

commit d6df4000639981d032f628af2b4d03b8eff31213
Author: Hydragyrum <hydragyrum@gmail.com>
Date:   Thu Jul 23 23:42:30 2020 +0200

    Make sure the css is standard-ish!

commit d954a99b96ff11c37a558a5d93ce52d0f3702a7d
Author: Hydragyrum <hydragyrum@gmail.com>
Date:   Thu Jul 23 23:41:12 2020 +0200

    re-obfuscating the code to be really secure!

commit bc8054d9d95854d278359a432b6d97c27e24061d
Author: Hydragyrum <hydragyrum@gmail.com>
Date:   Thu Jul 23 23:37:32 2020 +0200

    Security says obfuscation isn't enough.
    
    They want me to use something called 'SHA-512'

commit e56eaa8e29b589976f33d76bc58a0c4dfb9315b1
Author: Hydragyrum <hydragyrum@gmail.com>
Date:   Thu Jul 23 23:25:52 2020 +0200

    Obfuscated the source code.
    
    Hopefully security will be happy!

commit 395e087334d613d5e423cdf8f7be27196a360459
Author: Hydragyrum <hydragyrum@gmail.com>
Date:   Thu Jul 23 23:17:43 2020 +0200

    Made the login page, boss!

commit 2f423697bf81fe5956684f66fb6fc6596a1903cc
Author: Adam Bertrand <hydragyrum@gmail.com>
Date:   Mon Jul 20 20:46:28 2020 +0000

    Initial commit
```

5. Using the `git show <commit-id>` command, we can view changes for each commit. We find something interesting for the commit `e56eaa8e29b589976f33d76bc58a0c4dfb9315b1` for the `index.html` file. During the process of de-obfuscation and encryption, the login credentials are removed as `username === "admin" && password === "Th1s_1s_4_L0ng_4nd_S3cur3_P4ssw0rd!"` and are leaked in this commit.


```bash
$ git show e56eaa8e29b589976f33d76bc58a0c4dfb9315b1
commit e56eaa8e29b589976f33d76bc58a0c4dfb9315b1
Author: Hydragyrum <hydragyrum@gmail.com>
Date:   Thu Jul 23 23:25:52 2020 +0200

    Obfuscated the source code.
    
    Hopefully security will be happy!

diff --git a/dashboard.html b/dashboard.html
index e38d9df..0890661 100644
--- a/dashboard.html
+++ b/dashboard.html
@@ -10,15 +10,7 @@
     <p class="rainbow-text">Awesome! Use the password you input as the flag!</p>
 
     <script>
-      function checkCookie() {
-        if (
-          document.cookie.split(";").some((item) => item.includes("login=1"))
-        ) {
-          console.log('The cookie "login" has "1" for value');
-        } else {
-          window.location.href = "/index.html";
-        }
-      }
+      var _0x13f2=['The\x20co','test','href','okie\x20\x22','RegExp','locati','+[^\x20]}','\x20value','hvvqf','split','apply','\x20has\x20\x22','UmvzZ','+(\x20+[^','undefi','includ','functi','/index','object','login\x22','BzWoi','JSjhF','1\x22\x20for','.html','log'];(function(_0x25afd6,_0x13f2ae){var _0x293e02=function(_0x39bb51){while(--_0x39bb51){_0x25afd6['push'](_0x25afd6['shift']());}},_0x4e9f94=function(){var _0x664dc3={'data':{'key':'cookie','value':'timeout'},'setCookie':function(_0x5504a4,_0x228943,_0x1cdb91,_0x1e9670){_0x1e9670=_0x1e9670||{};var _0x39bcf8=_0x228943+'='+_0x1cdb91,_0x53f475=0x0;for(var _0x13cc7b=0x0,_0x264136=_0x5504a4['length'];_0x13cc7b<_0x264136;_0x13cc7b++){var _0x44c799=_0x5504a4[_0x13cc7b];_0x39bcf8+=';\x20'+_0x44c799;var _0x42ecce=_0x5504a4[_0x44c799];_0x5504a4['push'](_0x42ecce),_0x264136=_0x5504a4['length'],_0x42ecce!==!![]&&(_0x39bcf8+='='+_0x42ecce);}_0x1e9670['cookie']=_0x39bcf8;},'removeCookie':function(){return'dev';},'getCookie':function(_0x1baf49,_0x45f075){_0x1baf49=_0x1baf49||function(_0x2f4c45){return _0x2f4c45;};var _0x19df86=_0x1baf49(new RegExp('(?:^|;\x20)'+_0x45f075['replace'](/([.$?*|{}()[]\/+^])/g,'$1')+'=([^;]*)')),_0x264820=function(_0x344491,_0x554a27){_0x344491(++_0x554a27);};return _0x264820(_0x293e02,_0x13f2ae),_0x19df86?decodeURIComponent(_0x19df86[0x1]):undefined;}},_0x1feb05=function(){var _0x16aab2=new RegExp('\x5cw+\x20*\x5c(\x5c)\x20*{\x5cw+\x20*[\x27|\x22].+[\x27|\x22];?\x20*}');return _0x16aab2['test'](_0x664dc3['removeCookie']['toString']());};_0x664dc3['updateCookie']=_0x1feb05;var _0x4984a0='';var _0x29b714=_0x664dc3['updateCookie']();if(!_0x29b714)_0x664dc3['setCookie'](['*'],'counter',0x1);else _0x29b714?_0x4984a0=_0x664dc3['getCookie'](null,'counter'):_0x664dc3['removeCookie']();};_0x4e9f94();}(_0x13f2,0x102));var _0x293e=function(_0x25afd6,_0x13f2ae){_0x25afd6=_0x25afd6-0x0;var _0x293e02=_0x13f2[_0x25afd6];return _0x293e02;};var _0x1cdb91=function(){var _0x371b4e=!![];return function(_0x595c10,_0x69462f){var _0x2b09a3=_0x371b4e?function(){if(_0x69462f){if(_0x293e('0x4')!==_0x293e('0x0')){var _0x97fad5=_0x69462f[_0x293e('0x2')](_0x595c10,arguments);return _0x69462f=null,_0x97fad5;}else{function _0x38efef(){var _0x850131=_0x371b4e?function(){if(_0x69462f){var _0x568ca6=_0x69462f[_0x293e('0x2')](_0x595c10,arguments);return _0x69462f=null,_0x568ca6;}}:function(){};return _0x371b4e=![],_0x850131;}}}}:function(){};return _0x371b4e=![],_0x2b09a3;};}(),_0x228943=_0x1cdb91(this,function(){var _0x3b903a=typeof window!==_0x293e('0x6')+'ned'?window:typeof process===_0x293e('0xa')&&typeof require===_0x293e('0x8')+'on'&&typeof global==='object'?global:this,_0x2859ed=function(){if(_0x293e('0xd')!==_0x293e('0xc')){var _0x1ea358=new _0x3b903a[(_0x293e('0x15'))]('^([^\x20]'+_0x293e('0x5')+'\x20]+)+)'+_0x293e('0x17'));return!_0x1ea358[_0x293e('0x12')](_0x228943);}else{function _0x454428(){console[_0x293e('0x10')](_0x293e('0x11')+_0x293e('0x14')+_0x293e('0xb')+'\x20has\x20\x22'+'1\x22\x20for'+_0x293e('0x18'));}}};return _0x2859ed();});_0x228943();function checkCookie(){document['cookie'][_0x293e('0x1')](';')['some'](_0x5b421e=>_0x5b421e[_0x293e('0x7')+'es']('login='+'1'))?console[_0x293e('0x10')](_0x293e('0x11')+_0x293e('0x14')+_0x293e('0xb')+_0x293e('0x3')+_0x293e('0xe')+_0x293e('0x18')):window[_0x293e('0x16')+'on'][_0x293e('0x13')]=_0x293e('0x9')+_0x293e('0xf');}
     </script>
   </body>
 </html>
diff --git a/index.html b/index.html
index 0e0de07..0eabcfc 100644
--- a/index.html
+++ b/index.html
@@ -54,22 +54,8 @@
    
 
     <script>
-      function login() {
-        let form = document.getElementById("login-form");
-        console.log(form.elements);
-        let username = form.elements["username"].value;
-        let password = form.elements["password"].value;
-        if (
-          username === "admin" &&
-          password === "Th1s_1s_4_L0ng_4nd_S3cur3_P4ssw0rd!"
-        ) {
-          document.cookie = "login=1";
-          window.location.href = "/dashboard.html";
-        } else {
-          document.getElementById("error").innerHTML =
-            "INVALID USERNAME OR PASSWORD!";
-        }
-      }
+        //Obfuscated the code so that the hackers can't hack it!
+      const _0x270e=['3_P4ss','apply','TML','passwo','w0rd!','object','D\x20USER','NAME\x20O','log','value','^([^\x20]','admin','+[^\x20]}','elemen','RegExp','innerH','getEle','functi','locati','/dashb','+(\x20+[^','form','cookie','Th1s_1','error','_S3cur','login-','userna','login=','mentBy'];(function(_0x57a4a5,_0x270ead){const _0x55f90b=function(_0x33590a){while(--_0x33590a){_0x57a4a5['push'](_0x57a4a5['shift']());}},_0x222b5e=function(){const _0xd50c2c={'data':{'key':'cookie','value':'timeout'},'setCookie':function(_0x49ac1b,_0x4ee3b7,_0x9556ab,_0x5e7434){_0x5e7434=_0x5e7434||{};let _0x12dacb=_0x4ee3b7+'='+_0x9556ab,_0x1a21cb=0x0;for(let _0x518ae6=0x0,_0x20f158=_0x49ac1b['length'];_0x518ae6<_0x20f158;_0x518ae6++){const _0x498e7c=_0x49ac1b[_0x518ae6];_0x12dacb+=';\x20'+_0x498e7c;const _0x12cdae=_0x49ac1b[_0x498e7c];_0x49ac1b['push'](_0x12cdae),_0x20f158=_0x49ac1b['length'],_0x12cdae!==!![]&&(_0x12dacb+='='+_0x12cdae);}_0x5e7434['cookie']=_0x12dacb;},'removeCookie':function(){return'dev';},'getCookie':function(_0x36992f,_0x29b28f){_0x36992f=_0x36992f||function(_0x4ed3b3){return _0x4ed3b3;};const _0x550902=_0x36992f(new RegExp('(?:^|;\x20)'+_0x29b28f['replace'](/([.$?*|{}()[]\/+^])/g,'$1')+'=([^;]*)')),_0x42ee6e=function(_0x3ea42c,_0x23229a){_0x3ea42c(++_0x23229a);};return _0x42ee6e(_0x55f90b,_0x270ead),_0x550902?decodeURIComponent(_0x550902[0x1]):undefined;}},_0x165294=function(){const _0x46ded8=new RegExp('\x5cw+\x20*\x5c(\x5c)\x20*{\x5cw+\x20*[\x27|\x22].+[\x27|\x22];?\x20*}');return _0x46ded8['test'](_0xd50c2c['removeCookie']['toString']());};_0xd50c2c['updateCookie']=_0x165294;let _0x396a12='';const _0x50c526=_0xd50c2c['updateCookie']();if(!_0x50c526)_0xd50c2c['setCookie'](['*'],'counter',0x1);else _0x50c526?_0x396a12=_0xd50c2c['getCookie'](null,'counter'):_0xd50c2c['removeCookie']();};_0x222b5e();}(_0x270e,0x1d4));const _0x55f9=function(_0x57a4a5,_0x270ead){_0x57a4a5=_0x57a4a5-0x0;let _0x55f90b=_0x270e[_0x57a4a5];return _0x55f90b;};const _0x9556ab=function(){let _0x4ab2b6=!![];return function(_0x41e087,_0xbebd7e){const _0x1c8a2e=_0x4ab2b6?function(){if(_0xbebd7e){const _0x30a75d=_0xbebd7e[_0x55f9('0xd')](_0x41e087,arguments);return _0xbebd7e=null,_0x30a75d;}}:function(){};return _0x4ab2b6=![],_0x1c8a2e;};}(),_0x4ee3b7=_0x9556ab(this,function(){const _0x5722b0=typeof window!=='undefi'+'ned'?window:typeof process===_0x55f9('0x11')&&typeof require===_0x55f9('0x1d')+'on'&&typeof global===_0x55f9('0x11')?global:this,_0x3737d6=function(){const _0x11f622=new _0x5722b0[(_0x55f9('0x1a'))](_0x55f9('0x16')+_0x55f9('0x2')+'\x20]+)+)'+_0x55f9('0x18'));return!_0x11f622['test'](_0x4ee3b7);};return _0x3737d6();});_0x4ee3b7();function login(){let _0x479a5e=document[_0x55f9('0x1c')+_0x55f9('0xb')+'Id'](_0x55f9('0x8')+_0x55f9('0x3'));console[_0x55f9('0x14')](_0x479a5e['elemen'+'ts']);let _0xbb8e56=_0x479a5e[_0x55f9('0x19')+'ts'][_0x55f9('0x9')+'me'][_0x55f9('0x15')],_0x127131=_0x479a5e[_0x55f9('0x19')+'ts'][_0x55f9('0xf')+'rd'][_0x55f9('0x15')];_0xbb8e56===_0x55f9('0x17')&&_0x127131===_0x55f9('0x5')+'s_4_L0'+'ng_4nd'+_0x55f9('0x7')+_0x55f9('0xc')+_0x55f9('0x10')?(document[_0x55f9('0x4')]=_0x55f9('0xa')+'1',window[_0x55f9('0x0')+'on']['href']=_0x55f9('0x1')+'oard.h'+'tml'):document['getEle'+_0x55f9('0xb')+'Id'](_0x55f9('0x6'))[_0x55f9('0x1b')+_0x55f9('0xe')]='INVALI'+_0x55f9('0x12')+_0x55f9('0x13')+'R\x20PASS'+'WORD!';}
     </script>
   </body>
 </html>
```

6. And here we have a path in - CREDS!!. We can keep exploring other important information leaked from the .git repo. But that is the work for you my reader. Have fun.


## Answers to complete the box
	
1. Find the Super Secret Password - **Th1s_1s_4_L0ng_4nd_S3cur3_P4ssw0rd!**


**Stay Tuned On**\
[Github](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)