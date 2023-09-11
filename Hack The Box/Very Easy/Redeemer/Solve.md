# Write Up for Hack The Box box - [Redeemer](https://app.hackthebox.com/starting-point?tier=0)

Part of Starting Point Path. Guided Box

> Pratyush Prakhar (5#1NC#4N) - 08/25/2023


### TASKS

1. Which TCP port is open on the machine? - **6379** --> [nmap file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Redeemer/nmap/all.nmap)

2. Which service is running on the port that is open on the machine? - **redis** --> [nmap file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Redeemer/nmap/all.nmap)

3. What type of database is Redis? Choose from the following options: (i) In-memory Database, (ii) Traditional Database - **In-memory Database**

4. Which command-line utility is used to interact with the Redis server? Enter the program name you would enter into the terminal without any arguments. - **redis-cli**

5. Which flag is used with the Redis command-line utility to specify the hostname? - **-h**

6. Once connected to a Redis server, which command is used to obtain the information and statistics about the Redis server? - **INFO** --> [INFO file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Redeemer/redis/version.txt)

7. What is the version of the Redis server being used on the target machine? - **5.0.7** --> [Version file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Redeemer/redis/version.txt)

8. Which command is used to select the desired database in Redis? - **SELECT**

9. How many keys are present inside the database with index 0? --> `INFO keyspace` - **4**

10. Which command is used to obtain all the keys in a database? -  __KEYS *__

11. Submit root flag - **03e1d2b376c37ab3f5319922053953eb** --> [flag file](https://github.com/pratty010/Boxes/blob/master/Hack%20The%20Box/Very%20Easy/Redeemer/redis/flag.txt)
