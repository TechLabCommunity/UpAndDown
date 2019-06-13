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

counter = 0
container = []
while True:
    print(HEADER + "Starting scan all ips..." + ENDC)
    file = open(FILE_ADDRESSES, "r+")  # read the files with the name of host
    lines = file.readlines()
    sleep(WAITING)  # waiting some seconds.
    counter += 1
    if counter == TIMER:  # find again the UNKNOWN HOST after TIMER = 10
        del container[:]

    for index, host in enumerate(lines):
        ip = host.strip()  # delete "\n" and other some shits in the strings
        try:
            name_host = socket.gethostbyname(ip)
        except socket.gaierror:  # If you can't ping, hostname won't exist...
            name_host = "UNKNOWN"
        if is_pingable(ip):
            print(OKGREEN + "Success : " + ip + ": " + name_host + ENDC)
        elif index in container:  # don't do the else condition
            pass
        else:
            container.append(index)
            print(FAIL + "Fail : " + ip + ": " + name_host + ENDC)
            res = send_talent_mail(f"{name_host} is down!", password_gmail, "tommydzepina@gmail.com")
            if not res:
                print(WARNING + "Mail failed" + ENDC)
    file.close()


