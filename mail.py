import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart,MIMEBase
from email.encoders import *
import os
from celery import shared_task

SMTP_SERVER_HOST="localhost"
SMTP_SERVER_PORT=1025
SENDER_ADDRESS="nats@email.com"
SENDER_PASSWORD=""

# @shared_task
def send_email(to_address, subject, message, attachment):
    print("er0")
    mail=MIMEMultipart()
    mail["From"]=SENDER_ADDRESS
    mail["To"]=to_address
    mail["Subject"]=subject
    print("er1")
    mail.attach(MIMEText(message, "html"))
    print("er2")
    if attachment is not None:
        with open(attachment, "rb") as attachment_file:
            # adding file as an output stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_file.read())
            encode_base64(part)
        print("er3")
        part.add_header("Content-Disposition", f"attachment; filename={attachment[len('static/venue_detailsDownload/'):]}")
        mail.attach(part)
        print("er4")



    s=smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(mail)
    s.quit()
    print("er5")
    if attachment is not None:
        os.remove(attachment)
    print("er5")
    return True

# def main():
#     new_users=[
#         {"name":"Raj", "email":"raj@ex.com"},
#         {"name":"Rajat", "email":"rajat@ex.com"}
#     ]
#     for user in new_users:
#         send_email(to_address=user["email"], subject="Greetings", message=
#         "Welcome to Mailhog")

# if __name__=="__main__":
#     main()