# Write Up for Hack The Box box - [Responder](https://app.hackthebox.com/starting-point?tier=0)

Part of Starting Point Path. Guided Box

> Pratyush Prakhar (5#1NC#4N) - 08/25/2023


### TASKS

1. When visiting the web service using the IP address, what is the domain that we are being redirected to? - **unika.htb**
\
![](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Responder/images/redirect.png)

2. Which scripting language is being used on the server to generate webpages? - **PHP**
\
![](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Responder/images/php.png)

3. What is the name of the URL parameter which is used to load different language versions of the webpage?- **page**
\
![](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Responder/images/php.png)

4. Which of the following values for the `page` parameter would be an example of exploiting a Local File Include (LFI) vulnerability: "french.html", "//10.10.14.6/somefile", "../../../../../../../../windows/system32/drivers/etc/hosts", "minikatz.exe" - **../../../../../../../../windows/system32/drivers/etc/hosts**
\
![](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Responder/images/lfi.png)

5. Which of the following values for the `page` parameter would be an example of exploiting a Remote File Include (RFI) vulnerability: "french.html", "//10.10.14.6/somefile", "../../../../../../../../windows/system32/drivers/etc/hosts", "minikatz.exe" - **//10.10.14.6/somefile**

6. What does NTLM stand for? - **Windows New Technology LAN Manager** --> [NTLM Cheat Sheet](https://book.hacktricks.xyz/windows-hardening/ntlm)

7. Which flag do we use in the Responder utility to specify the network interface? - **-I** --> [responder file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Responder/ntlm/responder.md)

8. There are several tools that take a NetNTLMv2 challenge/response and try millions of passwords to see if any of them generate the same response. One such tool is often referred to as `john`, but the full name is what?. - **John The Ripper** --> [Hash File](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Responder/ntlm/Admin.hash)

9. What is the password for the administrator user? - **badminton** --> [Cracked Hash](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Responder/ntlm/Admin-cracked.hash)

10. We'll use a Windows service (i.e. running on the box) to remotely access the Responder machine using the password we recovered. What port TCP does it listen on? -  **5985** --> [nmap file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Responder/nmap/main.nmap)

11. Submit root flag - **ea81b7afddd03efaa0945333ed147fac** --> [flag file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Responder/ntlm/evil-winrm.md)
