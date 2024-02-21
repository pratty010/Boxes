import subprocess

def find_port(ip, user, l, h):
    while l <= h:
        port =  l + (h-l) // 2

        cmd = subprocess.run(
            ['ssh', '-o StrictHostKeyChecking=accept-new', '-p %s' %port, '%s@%s' %(user,ip)],
            stdout=subprocess.PIPE,
        )

        out = cmd.stdout.decode("utf-8")
        print(out)

        # If x is smaller, ignore right half
        if 'Lower' in out:
            l = port + 1
            print("port {} found with Lower keyword. Setting range to {} to {}.\n".format(port, l, h))
            
        # If x is greater, ignore right half
        elif 'Higher' in out:
            h = port - 1 
            print("port {} found with Higher keyword. Setting range to {} to {}.\n".format(port, l, h))
        # Check if x is present at mid
        else:
            print("port found at {}.\n".format(port))
            return port

    # If we reach here, then the element
    # was not present
    return -1


def main():
    ip = "10.10.191.151"
    user = "root"

    lower_port = 9000
    higher_port = 14000

    k = find_port(ip, user, lower_port, higher_port)

    if k == -1:
        print("no viable port found.")

if __name__ == '__main__':
    main()