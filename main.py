import socket
from subprocess import DEVNULL, STDOUT, check_output, CalledProcessError, Popen, PIPE
from time import sleep
from utils import send_talent_mail
import sys

if len(sys.argv) < 2:
    print("No password found")
    exit(1)

password_gmail = sys.argv[1].strip()
if not password_gmail:
    print("Password gmail is empty!")
    exit(10)

WAITING = 5
TIMER = 10
HOSTNAME_DNS = "8.8.8.8"
HOSTNAME_DNS_PORT = 80
FILE_ADDRESSES = "ip_addresses"

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def is_pingable(ip_address: str):
    process = Popen(["ping", "-c", "1", ip_address], stdout=PIPE, stderr=DEVNULL)
    return_code = process.wait()
    return return_code == 0


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((HOSTNAME_DNS, HOSTNAME_DNS_PORT))
my_ip = s.getsockname()[0]
print("current host: " + str(my_ip))
s.close()
file = open(FILE_ADDRESSES, "r+")  # read the files with the name of host
lines = file.readlines()

down = 0
while True:
    print(HEADER + "Starting scan all ips..." + ENDC)
    sleep(WAITING)  # waiting some seconds

    counter = 0
    for host in lines:
        ip = host.strip()
        if not is_pingable(ip):
            counter += 1  # how many hosts are down
            down_host = {str(ip): counter}
    down += 1  # how many time the the loop is repeated
    file.close()

    for host in lines:
        ip = host.strip()  # delete "\n" and other some shits in the strings
        try:
            name_host = socket.gethostbyname(ip)
        except socket.gaierror:  # If you can't ping, hostname won't exist...
            name_host = "UNKNOWN"
        if is_pingable(ip):
            print(OKGREEN + "Success : " + ip + ": " + name_host + ENDC)
        else:
            if down == 1:  # only first time print
                print(FAIL + "Fail : " + ip + ": " + name_host + ENDC)
                res = send_talent_mail(f"{name_host} is down!", password_gmail, "tommydzepina@gmail.com")
                if not res:
                    print(WARNING + "Mail failed" + ENDC)
            elif down == TIMER:  # reset the down counter and reopen the while loop with break
                down = 0
                break
    file.close()

