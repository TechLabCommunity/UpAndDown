import smtplib
from subprocess import DEVNULL, Popen, PIPE
from email.message import EmailMessage
from datetime import datetime

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


# function return true if status ok.
def get_status(domain: str):  # codice nuovo
    process = Popen(["whois", domain], stdout=PIPE, stderr=DEVNULL)
    results, _ = process.communicate()
    results = results.decode("utf-8")  # perchè devo convertire lista di byte in stringa con una certa codifica...
    marker = results.find("Status: ")
    line = results[marker:].strip()
    return "AVAILABLE" in line


def send_talent_mail(body: str, password: str, destination: str):
    gmail_user = 'alert@talent-lab.it'
    gmail_password = password
    from_addr = gmail_user
    to_addr = [destination]
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S, %d/%m/%Y")

    msg = EmailMessage()
    msg["Subject"] = "Python " + current_time
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(gmail_user, gmail_password)
            smtp.send_message(msg)
            smtp.close()
            return True
    except smtplib.SMTPAuthenticationError:
        print("Authentication Error. Username and password could be wrong.")
    except smtplib.SMTPHeloError:
        print("HELLO message failed.")
    return False
