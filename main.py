import socket
import sys
from subprocess import DEVNULL, Popen, PIPE
from time import sleep
import utils
from utils import get_status, is_pingable
from utils import send_talent_mail
from utils import local_host
 
print(sys.argv)

try:
    try_whois = Popen(["whois"], stdout=PIPE, stderr=DEVNULL)
    print("WHOIS command was found!")
except FileNotFoundError:
    print("WHOIS command was not found. You need to install whois command on your distro")
    exit(2)


if len(sys.argv) < 2:
    print("Need more arguments")
    exit(1)
elif len(sys.argv) == 3:
    if sys.argv[1] != "-f":
        print("il primo argumento non è -f quindi devi metterlo.")
        exit(11)
    else:
        file_da_aprire = sys.argv[2]
        print("qua devi mettere il codice che hai fatto")
        exit(0)
elif len(sys.argv) == 1:
    indirizzo_da_scandire = sys.argv[1]
    print("scansiona questo indirizzo...")
else:
    print("Too many arguments")
    exit(99)

WAITING = 5
TIMER = 10
HOSTNAME_DNS = "8.8.8.8"
HOSTNAME_DNS_PORT = 80
FILE_ADDRESSES = "ip_addresses"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((HOSTNAME_DNS, HOSTNAME_DNS_PORT))
my_ip = s.getsockname()[0]
print("current host: " + str(my_ip))
s.close()
file = open(FILE_ADDRESSES, "r")  # read the files with the name of host
lines = file.readlines()
file.close()

down = 0
while True:
    print(utils.HEADER + "Starting scan all ips..." + utils.ENDC)
    sleep(WAITING)  # waiting some seconds

    counter = 0
    for host in lines:
        ip = host.strip()
        if not is_pingable(ip):
            counter += 1  # how many hosts are down
            down_host = {str(ip): counter}
    down += 1  # how many time the the loop is repeated

    for host in lines:
        ip = host.strip()  # delete "\n" and other some shits in the strings
        try:
            name_host = socket.gethostbyname(ip)
        except socket.gaierror:  # If you can't ping, hostname won't exist...
            name_host = host

        if local_host(name_host):
            if is_pingable(ip):
                send_talent_mail(f"Local host {name_host} is pingable!", password_gmail, "tommydzepina@gmail.com")
            else:
                send_talent_mail(f"Local host {name_host} is not pingable!", password_gmail, "tommydzepina@gmail.com")
            #  if there is a local host but it's not pingable send the msg
            #  elif the host is not local and it's pingable send the msg
        elif is_pingable(ip):
            print(utils.OKGREEN + "Success : " + ip + ": " + name_host + utils.ENDC)
            # else, if the host is not local and the public domain is unknown send the msg
        else:
            if down == 1:  # only first time print
                print(utils.FAIL + "Fail : " + ip + ": " + name_host + utils.ENDC)
                res = send_talent_mail(f"{name_host} doesn't respond!", password_gmail, "tommydzepina@gmail.com")
                if not res:
                    print(utils.WARNING + "Mail failed" + utils.ENDC)
            elif down == TIMER:  # reset the down counter and reopen the while loop with break
                down = 0
                break

            if get_status(ip):
                send_talent_mail(f"{name_host} is AVAILABLE!", password_gmail, "tommydzepina@gmail.com")
                print(utils.OKGREEN + ip + " Status: is AVAILABLE.")

