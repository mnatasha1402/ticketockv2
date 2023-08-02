import time
from flask import session, redirect,url_for
from celery import shared_task


import os
import json
# from .timestamp import *
# from main import User,Admin,Booking,Show,Venue
# from .to_csv import *
import csv
from flask import send_file
from models import *
from json import dumps

from httplib2 import Http
#from celery_worker import *
from celery import current_app as celery_inst

# from mail import *
from celery.schedules import crontab
from jinja2 import Template
from monthly_report import *
# from .graph import *
from datetime import datetime as dt
from datetime import date

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import *
from email import encoders
import os

'''
A function which converts and returns the current time from datetime object to string in the HTML datetime-local format

Another function to perform the reverse action. Convert string to datetime object!

A 3rd function to give creation date 
'''


def current_timestamp():
    current_time = dt.now()
    datetime_str = current_time.strftime('%Y-%m-%dT%H:%M')  # Converts to a format of type - 2022-03-03T15:27
    return datetime_str  # returning the string formatted current time stamp


def convert_datetime(datetime_value):
    from datetime import datetime

    datetime_object = datetime.strptime(datetime_value, '%Y-%m-%dT%H:%M')  # 2022-03-03T15:27
    return datetime_object


def date_today():
    return date.today()

celery_inst.set_current()


@celery_inst.on_after_finalize.connect
def setup_intervalTASK(sender, **kwargs):
    sender.add_periodic_task(
        print("l1"),
        # crontab(minute=1),
        print("l2"),
        #crontab(minute=30, hour=17),  # Send a remainder every day at5.30pm IST
        print("l3"),
        webhook_chat.s(), name="daily at 5:30pm"

    )

    sender.add_periodic_task(
        print("l4"),
        # crontab(minute=1),
        #crontab(minute=30, hour=17, day_of_month=1),  # Send the monthly report every month at5.30pm IST
        print("l5"),
        monthly_report.s(),
        name="Monthly Report"
    )



def time(date):
        now = datetime.now() + timedelta(seconds = 60 * 3.4)
        return (timeago.format(date, now))

@shared_task
def monthly_report():
    print("r1")
    # last_month=(datetime.now()).month-1
    now = datetime.datetime.now()
    print("r2")
    month = now.strftime('%B')
    print("r3")
    year = now.strftime('%Y')
    print("r4")
    
    today = date_today().strftime('%Y-%m-%d')
    print("r5")
    users=User.query.all()
    print(users)
    with open(r"templates/report_mail_temp.html") as file:
        print("r6")
        msg_temp = Template(file.read())
        print("r7")

    with open(r"templates/report.html") as file:
        print("r8")
        pdf_temp = Template(file.read())
        print("r9")

    done_users = []
    print("r10")
    for user_obj in users:
        print("r11")
        user = user_obj.username
        print(user)
        print("r12")
        account_details = accountDetails(user_obj)  # Function returns all required account details
        print("r13")
        bookings = bookingDetails(user_obj)  
        print("r14")
        
        message = msg_temp.render(user=user)
        print("r15")
        pdf_html = pdf_temp.render(today=str(today),
                                   month=month,
                                   account_details=account_details,
                                   bookings=bookings,
                                   
                                   username=user
                                   )
        print("r16")
        sub = f"[MONTHLY REPORT] Ticketocks"
        print("r17")
        if user not in done_users:
            pdf_path = generate_pdf(usr=user, template=pdf_html)
            print("r17.1")
            send_email(to_address=user_obj.email, subject=sub, message=message, attachment=pdf_path)
            print("r17.2")
            done_users.append(user)
        print("r18")

        print(f"------MONTHLY REPORT SENT FOR {user}---------")
        print("r19")
    return("report sent")


# @celery_inst.task()
# def send_remainder():
#     users = USER.query.all()
#     user_email = {user.username: [user.email, user.last_log] for user in users}
#     send_reminder_to = {}

#     today = current_timestamp()[:current_timestamp().index("T")]

#     for k, v in user_email.items():
#         if v[1].find(today) == -1:  # If the value was not logged today
#             send_reminder_to[k] = v[0]

#     # send_reminder_to now contains all the users who did not log to any tracker today.

#     with open(r"templates/email_templates/daily_reminder.html") as file:
#         temp = Template(file.read())

#     for user, email_id in send_reminder_to.items():
#         message = temp.render(user=user)
#         sub = f"[REMAINDER] LYF-RECORD: QUANTIFIED-SELF APP"
#         send_email(email_id, subject=sub, msg=message)

#     return {"msg": "Successful"}

def export_venue_to_csv(venue):
    print("dvdline01x")
    filename = "venue_" + current_timestamp() + ".csv"
    print("dvdline0x")
    filepath = f"static/venue_detailsDownload/{filename}"
    print("dvdline1x")
    with open(filepath, 'w', newline='') as venue_file:
        fieldnames = ['venue_id', 'venue_name', 'venue_place', 'venue_capacity']
        print("dvdline2x")
        csv_writer = csv.DictWriter(venue_file, fieldnames=fieldnames)
        print("dvdline3x")
        csv_writer.writeheader()
        csv_writer.writerow({
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_place': venue.place,
            'venue_capacity': venue.capacity,
        })
        print("dvdline4x")

    return filepath

@celery_inst.task()
def download_venueDetails(venue_id, username=None):
    if username is not None:
        venue_details = None
        try:
            #print("dvdline0")
            print(username)
            #print(Admin.query.all())
            admin=Admin.query.filter_by(username=username).first()
            print(admin)
            to_email = admin.email
            print(to_email)
            #print("dvdline1")
            venue = Venue.query.filter_by(id=venue_id).first()
            print("dvdline2")
            filepath = export_venue_to_csv(venue)
            print("dvdline3")
            with open(r"templates/download_ready.html") as file:
                temp = Template(file.read())
            print("dvdline4")
            sub = "[Venue Details DOWNLOAD READY] Ticketocks"
            print("dvdline5")
            message = temp.render(user=username,venue=venue.name, file_type="Venue data")
            print(message)
            print("dvdline6")
            send_email(to_address=to_email, subject=sub, message=message, attachment=filepath)
            print("dvdline7")

            return {"msg": "Successful"}, 200

        except:
            return {"msg": "Failed1"}
    else:
        return {"msg": "Failed2"}

 

SMTP_SERVER_HOST="localhost"

SMTP_SERVER_PORT="1025"
SENDER_ADDRESS="nats@email.com"
SENDER_PASSWORD=""
global s
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
        print("er2.1")
        with open(attachment, "rb") as attachment_file:
            print("er2.2")
            part = MIMEBase("application", "octet-stream")
            print("er2.3")
            part.set_payload(attachment_file.read())
            print("er2.4")
            encoders.encode_base64(part)
            print("er2.5")
            part.add_header("Content-Disposition", f"attachment; filename={attachment[len('static/venue_detailsDownload/'):]}")
            mail.attach(part)
            print("er3")
    print("er4")
    s=smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    print("er4.1")
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    print("er4.2")
    s.send_message(mail)
    print("er4.3")
    s.quit()
    print("er4")
    if attachment is not None:
        abs_attachment_path = os.path.abspath(attachment)
        os.remove(abs_attachment_path)
    print("er5")

    return True


# @celery_inst.task()
@shared_task
def webhook_chat():
    #print("w1")
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    #print("w2"),
    http_obj = Http()
    #print("w3")
    data = {'text': 'Reminder: Please visit/book something.'}
    #print("w4")

    res = http_obj.request('https://chat.googleapis.com/v1/spaces/AAAAUd0jbA4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=cOvvegHU-6uaTw2p3JObbQ6thy4mXqKZcf34x2qtIQ8', method='POST', headers=message_headers, body=dumps(data))
    #print("w5")
    print("Reminder sent. Response:", res)



# WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAUd0jbA4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=cOvvegHU-6uaTw2p3JObbQ6thy4mXqKZcf34x2qtIQ8"

# def main():
#     """Google Chat incoming webhook quickstart."""
#     url = WEBHOOK_URL
#     app_message = {
#         'text': 'Reminder: Please visit/book something.'}
#     message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
#     http_obj = Http()
#     response = http_obj.request(
#         uri=url,
#         method='POST',
#         headers=message_headers,
#         body=dumps(app_message),
#     )
#     print(response)
    
# # ********** GENERATE_CSV********
# @celery.task(name='venue_report')
# def generate_csv(user_id):
#     posts=Post.query.filter_by(user_id=user_id).order_by(Post.timestamp.desc()).all() 
      
#     with open(f'static/post.csv','w') as post_csv:
#         for i in range(len(posts)):
#             post = posts[i]
           
#             post_csv.write(f'{i+1},{post.body},{time(post.timestamp)}\n')



# # *********  DOWNLOAD POST CSV ***************
# @app.route("/download-file")
# def download_file():
#     return send_file("static/post.csv")






