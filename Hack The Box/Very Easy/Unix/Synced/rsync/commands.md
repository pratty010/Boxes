```bash
$rsync --list-only 10.129.228.37::
public          Anonymous Share
┌─[ace@parrot]─[~/Desktop/Git_work/Boxes/Hack The Box/Very Easy/Synced]
└──╼ $rsync --list-only 10.129.228.37::public
drwxr-xr-x          4,096 2022/10/24 18:02:23 .
-rw-r--r--             33 2022/10/24 17:32:03 flag.txt
┌─[ace@parrot]─[~/Desktop/Git_work/Boxes/Hack The Box/Very Easy/Synced]
└──╼ $rsync --list-only 10.129.228.37::"Anonymous Share"
@ERROR: Unknown module 'Anonymous Share'
rsync error: error starting client-server protocol (code 5) at main.c(1863) [Receiver=3.2.7]
┌─[✗]─[ace@parrot]─[~/Desktop/Git_work/Boxes/Hack The Box/Very Easy/Synced]
└──╼ $rsync --list-only 10.129.228.37::Anonymous\ Share
@ERROR: Unknown module 'Anonymous Share'
rsync error: error starting client-server protocol (code 5) at main.c(1863) [Receiver=3.2.7]
┌─[✗]─[ace@parrot]─[~/Desktop/Git_work/Boxes/Hack The Box/Very Easy/Synced]
└──╼ $rsync 10.129.228.37::public/flag.txt flag.txt
```