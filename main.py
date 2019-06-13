import socket
from subprocess import DEVNULL, STDOUT, check_output, CalledProcessError, Popen, PIPE
from time import sleep

WAITING = 5 
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

while True:
    print(HEADER + "Starting scan all ips..." + ENDC)
    file = open(FILE_ADDRESSES, "r")  # read the files with the name of host
    sleep(WAITING)  # waiting some seconds.
    for line in file:
        ip = line.strip()  # delete "\n" and other some shits in the strings
        try:
            name_host = socket.gethostbyname(ip)
        except socket.gaierror:  # If you can't ping, hostname won't exist...
            name_host = "UNKNOWN"
        if is_pingable(ip):
            print(OKGREEN + "Success : " + ip + ": " + name_host + ENDC)
        else:
            print(FAIL + "Fail : " + ip + ": " + name_host + ENDC)
    file.close()
