import json
import smtplib
from subprocess import DEVNULL, Popen, PIPE
from email.message import EmailMessage
from datetime import datetime
import socket

HOSTNAME_DNS = "8.8.8.8"
HOSTNAME_DNS_PORT = 80


def get_value_config(key: str):
    json_config = json.load(open("config.json", "r"))
    return json_config[key]


def is_pingable(ip_address: str):
    process = Popen(["ping", "-c", "1", ip_address], stdout=PIPE, stderr=DEVNULL)
    return_code = process.wait()
    return return_code == 0


# function return true if status ok.
def get_whois_status(domain: str):  # codice nuovo
    process = Popen(["whois", domain], stdout=PIPE, stderr=DEVNULL)
    results, _ = process.communicate()
    results = results.decode("utf-8")  # perchè devo convertire lista di byte in stringa con una certa codifica...
    marker = results.find("Status: ")
    return "AVAILABLE" in results[marker:].strip().upper()


def is_local_address(local_host_ip: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((HOSTNAME_DNS, HOSTNAME_DNS_PORT))
    ip = s.getsockname()[0]
    s.close()

    all_occ = [i for i, letter in enumerate(ip) if letter == "."]
    last_occ = all_occ[-1]
    ip_castrato = ip[:last_occ + 1]
    return ip_castrato == local_host_ip[:12]


def send_talent_mail(body: str, password: str, destination: str):
    gmail_user = 'alert@talent-lab.it'
    gmail_password = password
    from_addr = gmail_user
    to_addr = [destination]
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S, %d/%m/%Y")

    msg = EmailMessage()
    msg["Subject"] = "Python UpAndDown " + current_time
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(body)

    try:
        hostname_smtp = get_value_config("HOSTNAME_SMTP")
        port_smtp = int(get_value_config("PORT_SMTP"))
        with smtplib.SMTP(hostname_smtp, port_smtp) as smtp:
            smtp.login(gmail_user, gmail_password)
            smtp.send_message(msg)
            smtp.close()
            return True
    except smtplib.SMTPAuthenticationError:
        print("Authentication Error. Username and password could be wrong.")
    except smtplib.SMTPHeloError:
        print("HELLO message failed.")
    return False
