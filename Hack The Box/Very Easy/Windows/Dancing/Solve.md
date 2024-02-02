# Write Up for Hack The Box box - [Dancing](https://app.hackthebox.com/starting-point?tier=0)

Part of Starting Point. Guided Box

> Pratyush Prakhar (5#1NC#4N) - 08/25/2023


### TASKS

1. What does the 3-letter acronym SMB stand for? - **Server Message Block**

2. What port does SMB use to operate at? - **445**

3. What is the service name for port 445 that came up in our Nmap scan? - **microsoft-ds** --> [nmap file](nmap/main.nmap)

4. What is the 'flag' or 'switch' that we can use with the smbclient utility to 'list' the available shares on Dancing? - **smbclient -L** --> [Shares file](smb/share.out)

5. How many shares are there on Dancing? - **4**

6. What is the name of the share we are able to access in the end with a blank password? - **WorkShares** --> [WorkSpaces Dir](smb/WorkSpaces)

7. What is the command we can use within the SMB shell to download the files we find? - **get** 

8. Submit root flag - **5f61c10dffbc77a704d76016a22f1664** --> [flag file](smb/WorkSpaces/James.P/flag.txt)
