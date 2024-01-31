# Write Up for Hack The Box box - [Tactics](https://app.hackthebox.com/starting-point?tier=1)

Part of Starting Point Path. Guided Box

> Pratyush Prakhar (5#1NC#4N) - 01/31/2024


### TASKS

1. Which Nmap switch can we use to enumerate machines when our ping ICMP packets are blocked by the Windows firewall? - **-Pn** --> [rust file](rustscan/main.nmap)

2. What does the 3-letter acronym SMB stand for? - **Server Message Block** --> [useful link](https://aws.amazon.com/compare/the-difference-between-nfs-smb/)

3. What port does SMB use to operate at? - **139/445**

4. What command line argument do you give to `smbclient` to list available shares? - **-L**

5. What character at the end of a share name indicates it's an administrative share? - **$** -

6. Which Administrative share is accessible on the box that allows users to view the whole file system? - **C$** --> [SMB Administrator shares](smb/smbmap.txt)

7. What command can we use to download the files we find on the SMB Share? - **get** --> [manual mode](smb/smbclient.txt)

8. Which tool that is part of the Impacket collection can be used to get an interactive shell on the system? - **psexec.py/smbexec.py**

9. Submit root flag - **f751c19eda8f61ce81827e6930a1f40c** --> [Desktop Flag file](smb/flag.txt)
