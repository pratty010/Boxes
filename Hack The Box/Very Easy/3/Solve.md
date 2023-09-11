# Write Up for Hack The Box box - [Three](https://app.hackthebox.com/starting-point?tier=1)

Part of Starting Point Path. Guided Box

> Pratyush Prakhar (5#1NC#4N) - 09/09/2023


### TASKS

1. How many TCP ports are open? - **2** --> [nmap file](https://github.com/pratty010/Boxes/tree/master/Hack%20The%20Box/Very%20Easy/3/nmap/all.nmap)

2. What is the domain of the email address provided in the "Contact" section of the website? - **thetoppers.htb**
![](https://github.com/pratty010/Boxes/tree/master/Hack%20The%20Box/Very%20Easy/3/images/domain.png)

3. In the absence of a DNS server, which Linux file can we use to resolve hostnames to IP addresses in order to be able to access the websites that point to those hostnames? - **/etc/hosts**

4. Which sub-domain is discovered during further enumeration? - **s3.thetoppers.htb** --> [dirb file](https://github.com/pratty010/Boxes/tree/master/Hack%20The%20Box/Very%20Easy/3/web/main.out)

5. Which service is running on the discovered sub-domain?- **Amazon S3**

6. Which command line utility can be used to interact with the service running on the discovered sub-domain?- **awscli**

7. Which command is used to set up the AWS CLI installation? - **aws configure** 

8. What is the command used by the above utility to list all of the S3 buckets? - **aws s3 ls**

9. This server is configured to run files written in what web scripting language? - **PHP**
![](https://github.com/pratty010/Boxes/tree/master/Hack%20The%20Box/Very%20Easy/3/images/awslfi.png)\
![](https://github.com/pratty010/Boxes/tree/master/Hack%20The%20Box/Very%20Easy/3/images/phpcmd.png)

10. Submit root flag - **a980d99281a28d638ac68b9bf9453c2b** 
![](https://github.com/pratty010/Boxes/tree/master/Hack%20The%20Box/Very%20Easy/3/images/flag.png)
