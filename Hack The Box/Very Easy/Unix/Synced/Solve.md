# Write Up for Hack The Box box - [Synced](https://app.hackthebox.com/starting-point?tier=0)

Part of Starting Point. Very Easy, Guided Box

> Pratyush Prakhar (5#1NC#4N) - 09/28/2023


### TASKS

1. What is the default port for rsync?- **873** --> [nmap file](rustscan/intial.nmap)

2. How many TCP ports are open on the remote host? - **1** --> [nmap file](rustscan/all.nmap)

3. What is the protocol version used by rsync on the remote machine? - **31** --> [nmap main file](rustscan/main.nmap)

4. What is the most common command name on Linux to interact with rsync? - **rsync**

5. What credentials do you have to pass to rsync in order to use anonymous authentication? anonymous:anonymous, anonymous, None, rsync:rsync. - **None**

6. What is the option to only list shares and files on rsync? (No need to include the leading -- characters) - **list-only** --> [rsync file](rsync/commands.md)

7. Submit root flag - **72eaf5344ebb84908ae543a719830519** --> [flag file](rsync/public/flag.txt)

