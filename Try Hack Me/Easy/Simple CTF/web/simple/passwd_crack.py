import hashlib


def crack_passwd(salt, hash):

    password_file = open("/usr/share/seclists/Passwords/Common-Credentials/best110.txt", "r")

    for password in password_file.readlines():
        passwd = password.replace("\n", "")
        print "[!] Trying password : " + passwd

        if hashlib.md5(salt+passwd).hexdigest() == hash:
            print "[+] Cracked Password : " + passwd
            break
    
    password_file.close()


crack_passwd('1dac0d92e9fa6bb2', '0c01f4468bd75d7a84c7eb73846e8d96')

# [+] Cracked Password : secret