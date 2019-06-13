import smtplib
import sys


def send_talent_mail(body: str, password: str, destination: str):
    gmail_user = 'alert@talent-lab.it'
    gmail_password = password

    sent_from = gmail_user
    to = [destination]
    subject = 'Alert da parte di Up and Down'

    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s
    
    %s
    """ % (sent_from, ", ".join(to), subject, body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        return True
    except:
        return False
