# Write Up for Hack The Box box - [Mongod](https://app.hackthebox.com/starting-point?tier=0)

Part of Starting Point. Very Easy, Guided Box

> Pratyush Prakhar (5#1NC#4N) - 09/22/2023


### TASKS

1. How many TCP ports are open on the machine? - **2** --> [nmap file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Meow/nmap/main.nmap)

2. Which service is running on port 27017 of the remote host? - **MongoDB 3.6.8**  --> [nmap file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Meow/nmap/main.nmap)

3. What type of database is MongoDB? (Choose: SQL or NoSQL) - **NoSQL**

4. What is the command name for the Mongo shell that is installed with the mongodb-clients package? - **mongo**

5. What is the command used for listing all the databases present on the MongoDB server? (No need to include a trailing ;) - **show dbs**

6. What is the command used for listing out the collections in a database? (No need to include a trailing ;) - **show collections** 

7. What is the command used for dumping the content of all the documents within the collection named flag in a format that is easy to read? - **db.flag.find().pretty()** 

8. Submit root flag - **1b6e6fb359e7c40241b6d431427ba6ea** --> [flag collection](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Meow/telnet/root.bash)
