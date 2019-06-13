import socket
from subprocess import DEVNULL, STDOUT, check_output, CalledProcessError, Popen, PIPE
from time import sleep


START_INDEX = 18
STOP_INDEX = 27
HOSTNAME_DNS = "8.8.8.8"
HOSTNAME_DNS_PORT = 80

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((HOSTNAME_DNS, HOSTNAME_DNS_PORT))
ip = s.getsockname()[0]
print("current host: " + str(ip))

all_occ = [i for i, letter in enumerate(ip) if letter == "."]
last_occ = all_occ[-1]
ip_castrato = ip[:last_occ + 1]
counter = 0
counter_1 = 0
final_list = []

while True:
    print("Starting scan all ips...")
    sleep(5)  # waiting some seconds.
    for i in range(START_INDEX, STOP_INDEX):
        # ping attraversso il sistema
        process = Popen(["ping", "-c", "1", ip_castrato + str(i)], stdout=PIPE)
        return_code = process.wait()
        if return_code == 0:
            counter += 1
            try:
                name_host = socket.gethostbyaddr(ip_castrato + str(i))
            except socket.herror:
                name_host = "HOST non riconosciuto"
            list_host = list(name_host)

            # elimino le parentesi quadre che sono in mezzo
            if type(list_host) is list and [] in list_host:
                list_host.remove([])
                final_list.append(str(list_host)[1:-1])
                if return_code == 0:
                    print(str(list_host)[1:-1] + " is up!")

        # indirizzi ip liberi
        else:
            counter_1 += 1
            print(ip_castrato + str(i), " is down!")

    # non serve mettere queste istruzioni dentro il ciclo for, bastano fuori...
    # qunatita di host attivi e indirizzi ip liberi
    print("\nNot active hosts: " + str(counter_1))
    print("Active hosts: " + str(counter))

    # host ordinati per colonne
    for item in final_list:
        print(str("\n" + item) + "\n")

