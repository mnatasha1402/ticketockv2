import os
from models import *
import datetime
from datetime import datetime as dt
from datetime import date
from flask import Flask,render_template, url_for

# from weasyprint import HTML
# from main import User,Admin,Booking,Show,Venue
import pdfkit

# base_url='http://127.0.0.1:8001/'
# wkhtmltopdf_path='/mnt/c/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
wkhtmltopdf_path='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'

# pdfkit_config = {
#     'wkhtmltopdf': wkhtmltopdf_path
# }
pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)


def accountDetails(user):
    print(user)
    account_details = {}
    # user = User.query.filter_by(username=user)    
    print(user)
    account_details["id"]= user.id,
    account_details["username"]=user.username,
    account_details["email"]=user.email,
    account_details["bookings"]=[booking.to_dict() for booking in user.bookings]

    return account_details
           
    # export PATH="C:\Program Files\wkhtmltopdf\bin:$PATH"
  
    # # ----------------------
    # # Username -->
    # account_details["username"] = USER.query.filter_by(username=user).first()
    # # ----------------------
    # # Streak count -->
    # account_details["streak"] = STREAK.query.filter_by(username=user).first().count
    # # ----------------------
    # # Trackers count -->
    # trackers = USER_TRACKER.query.filter_by(username=user).distinct()
    # tracker_count = 0
    # for i in trackers:
    #     tracker_count += 1
    # account_details["No. of trackers"] = tracker_count
    # # ----------------------
    # # Member since -->
    # member_create = USER.query.filter_by(username=user).first()
    # member_since = str(datetime.datetime.today() - datetime.datetime.strptime(member_create.creation, '%Y-%m-%d'))
    # member_since = member_since.split(",")
    # account_details["Member Since"] = member_since[0]
    # # ----------------------
    # # Last logged
    # account_details["last_logged"] = USER.query.filter_by(username=user).first().last_log
    # # ----------------------
    # return account_details


def bookingDetails(user):
    # user = User.query.get(user_id) 
    bookings=[booking.to_dict() for booking in user.bookings]
    # tracker_ids = USER_TRACKER.query.filter_by(username=user).distinct()
    # trackers = [TRACKER.query.filter_by(tracker_id=t_id.tracker_id).first() for t_id in tracker_ids]
    return bookings



def generate_pdf(usr, template):
    month = date_today().strftime("%B")
    file_name = f"static/user_monthly_reports/monthly_report_{str(usr)}_{month}.pdf"
    # rendered_template = render_template('report.html', url_for=url_for, other_variable=other_value)
    pdfkit.from_string(template, f'{file_name}',configuration=pdfkit_config)
    # pdfkit.from_string(template, f'{file_name}')
    

    return file_name

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