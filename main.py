import socket
import sys
from subprocess import DEVNULL, Popen, PIPE
from time import sleep
from utils import get_whois_status, is_pingable
from utils import send_talent_mail
from utils import is_local_address
from logging import debug, error, info, warning, critical
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

try:
    try_whois = Popen(["whois"], stdout=PIPE, stderr=DEVNULL)
    info("WHOIS command was found!")
except FileNotFoundError:
    critical("WHOIS command was not found. You need to install whois command on your distro")
    exit(2)


WAITING = 5
HOSTNAME_DNS = "8.8.8.8"
HOSTNAME_DNS_PORT = 80

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((HOSTNAME_DNS, HOSTNAME_DNS_PORT))
my_ip = s.getsockname()[0]
info("current host: " + str(my_ip))
s.close()


def check_complete_status(hostnames: tuple):
    info("Starting scan all ips...")
    sleep(WAITING)  # waiting some seconds

    for host in hostnames:
        host = host.strip()  # delete "\n" and other some shits in the strings

        if not is_pingable(host):
            error(f"{host} is not pingable")
            send_talent_mail(f"{host} is not pingable!", "", "tommydzepina@gmail.com")
            return
        if not is_local_address(host):
            try:
                name_host = socket.gethostbyname(host)
                info("Name Host is : " + host + ": " + name_host)
            except socket.gaierror:  # If you can't ping, hostname won't exist...
                name_host = host
                error(f"Name host {name_host} can't be resolved!")
                send_talent_mail(f"Name host {name_host} can't be resolved!", "", "tommydzepina@gmail.com")
                return
                # else, if the host is not local and the public domain is unknown send the msg
        elif not get_whois_status(host):
                send_talent_mail(f"{name_host} is NOT AVAILABLE!", "", "tommydzepina@gmail.com")
                print(host + " Status: is not AVAILABLE.")
        else:
            info("Name Host : " + host + " with no errors")


if __name__ == '__main__':
    if len(sys.argv) < 2:  # if you tipe nothing exit
        print("Need more arguments")
        exit(1)
    elif len(sys.argv) == 2:  # if third element is empty exit
        host_to_check = (sys.argv[1])
        check_complete_status(host_to_check)
        exit(11)
    elif len(sys.argv) == 3:  # check right element
        if sys.argv[1] != "-f":
            print("the first is invalid.")
        else:
            file = open(sys.argv[2], "r")  # read the files with the name of host
            lines = file.readlines()
            file.close()
            check_complete_status(tuple(lines))
            exit(0)
    else:
        print("Too many arguments")
        exit(99)
