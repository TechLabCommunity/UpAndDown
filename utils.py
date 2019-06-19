import smtplib
from email.message import EmailMessage
from datetime import datetime


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
















