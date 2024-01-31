# Write Up for Hack The Box box - [Explosion](https://app.hackthebox.com/starting-point?tier=0)

Part of Starting Point Path. Guided Box

> Pratyush Prakhar (5#1NC#4N) - 01/31/2024


### TASKS

1. What does the 3-letter acronym RDP stand for? - **Remote Desktop Protocol**

2. What is a 3-letter acronym that refers to interaction with the host through a command line interface? - **cli**

3. What about graphical user interface interactions? - **GUI**

4. What is the name of an old remote access tool that came without encryption by default and listens on TCP port 23? - **telnet**

5. What is the name of the service running on port 3389 TCP? - **ms-wbt-server** --> [nmap file](rustscan/main.nmap)

6. What is the switch used to specify the target host's IP address when using xfreerdp? - **/v:** -->  xfreerdp help or man page.

7. What username successfully returns a desktop projection to us with a blank password? - **Administrator** - default creds.

8. Submit root flag - **951fa96d7830c451b536be5a6be008a0** - On the main `Desktop`.
