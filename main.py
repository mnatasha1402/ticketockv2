from flask import Flask, abort, render_template,url_for,request,redirect,flash, jsonify,request
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager,login_required, login_user, logout_user, current_user
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt,get_jwt_identity
#from sqlalchemy.orm import relationship
from datetime import datetime
from flask_restful import Resource, reqparse,Api
from flask import jsonify, make_response
from flask_cors import CORS
from time import sleep
import time
import logging
import os
import json
import csv
from flask import session, redirect,url_for
# from celery import Celery
from flask import send_file
# from models import *
from json import dumps
from httplib2 import Http
from datetime import datetime as dt
from datetime import date

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import *
from email import encoders

from models import *
from mail import *
from monthly_report import *
# from cache_instance import current_cache_inst as cache


from celery import shared_task
from celery import Celery, Task
from celery.schedules import crontab
# from cache_instance import current_cache_inst as cache
from jinja2 import Template
# from flask_caching import Cache


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def _call_(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask,broker=app.config['CELERY_BROKER_URL'])
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'secret-key'
app.config['CELERY_BROKER_URL'] = 'redis://localhost'
app.config['result_backend'] = 'redis://localhost'
app.config["CACHE_TYPE"]="RedisCache"
app.config["CACHE_REDIS_HOST"]= "localhost"
app.config["CACHE_REDIS_PORT"]= 6379
api = Api(app)
CORS(app)
jwt = JWTManager(app)
# db = SQLAlchemy(app)
db.init_app(app)
migrate=Migrate(app,db)

# app.config.from_mapping(cache_mapping)  # Setup Redis Cache
cache = Cache(app)  # cache instance
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery = celery_init_app(app)
celery.conf.update(app.config)
    
celery.conf.beat_schedule = {
"my_function_every_1_minutes": {
    "task": "monthly_report",
    "schedule": crontab(minute="*/1"),
    # "schedule": crontab(minute="0", hour="0", day="last", month="*"),
},
"my_function_every_2_minutes": {
    "task": "webhook",
    "schedule": crontab(minute="*/1"),
    # "schedule": crontab(minute="59", hour="23", day="*"),
},
}


# dt_str = booking_time.isoformat()

# # Serialize to JSON
# data = {'datetime': dt_str}
# json_data = json.dumps(data)

class Home(Resource):
    def get(self):
        return {
            "heading": "Welcome to Ticketocks"
            }

# @app.route("/")
# def index():
#     return render_template("index.html")

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        user_type=data.get('user_type')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if user_type == "user":
            data = User.query.filter_by(username=username).first()
            if data is None:
                user = User(username=username, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                return {'message': 'User created'}, 201
            else:
                return {'message': 'User already exists'}, 400

        if user_type == "admin":
            data = Admin.query.filter_by(username=username).first()
            if data is None:
                admin = Admin(username=username, email=email)
                admin.set_password(password)
                db.session.add(admin)
                db.session.commit()
                return {'message': 'Admin created'}, 201
            else:
                return {'message': 'Admin already exists'}, 400

class AdminLoginResource(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            access_token = create_access_token(identity=admin.id)
            return {'access_token': access_token,'admin_id':admin.id}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

    # @cache.memoize(1000)
    def get(self, admin_id):
        # Fetch the user details using the user ID
        admin = Admin.query.get(admin_id)

        if admin:
            # Return the user details as a dictionary
            return {
                'id': admin.id,
                'username': admin.username,
                'email': admin.email,
                'venues': [venue.to_dict() for venue in admin.venues],
                'shows': [show.to_dict() for show in admin.shows]
                # Add more user details here as needed
            }, 200
        else:
            return {'message': 'Admin not found'}, 404

    def delete(self, admin_id):
        # Fetch the user details using the user ID
        admin = Admin.query.get(admin_id)

        if admin:
            # Delete the user from the database
            db.session.delete(admin)
            db.session.commit()

            return {'message': 'admin deleted successfully'}, 200
        else:
            return {'message': 'admin not found'}, 404

class UserLoginResource(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        print (username, password)
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token,'userid':user.id}, 200

        else:
            return {'message': 'Invalid credentials'}, 401

    # @cache.memoize(1000)
    def get(self, user_id):
        # Fetch the user details using the user ID
        user = User.query.get(user_id)

        if user:
            # Return the user details as a dictionary
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bookings':[booking.to_dict() for booking in user.bookings]
                # Add more user details here as needed
            }, 200
        else:
            return {'message': 'User not found'}, 404

    def delete(self, user_id):
        # Fetch the user details using the user ID
        user = User.query.get(user_id)

        if user:
            # Delete the user from the database
            current_session = db.session.object_session(user)
            if current_session is not None and current_session != db.session:
            # Detach the booking from the old session
                current_session.expunge(user)
            db.session.delete(user)
            db.session.commit()

            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User not found'}, 404


@login_manager.user_loader
def load_user(id):
    # Check if the user is a customer
    user = User.query.get(int(id))
    if user:
        return user

    # Check if the user is an admin
    user = Admin.query.get(int(id))
    if user:
        return user
    
    return None

class Logout(Resource):
    @jwt_required()
    def post(self):
        
        revoked_tokens()
        logout_user()
        return {'message': 'Successfully logged out'}, 200

class VenueResource(Resource):
    @jwt_required()
    def get(self, venue_id=None):
        admin_id = get_jwt_identity()

        if venue_id:
            venue = Venue.query.get(venue_id)
            if not venue:
                return {'message': 'Venue not found'}, 404

            return {
                'venue': {
                    'id': venue.id,
                    'name': venue.name,
                    'place': venue.place,
                    'capacity': venue.capacity,
                    'admin_id': venue.admin_id,
                    'shows': [show.to_dict() for show in venue.shows]
                }
            }, 200

        # If neither venue_id nor admin_id is provided, return all venues
        venues = Venue.query.all()
        if venues:
            return {'venues': [venue.to_dict() for venue in venues]}, 200

        return {'message': 'Venue not found'}, 404

        # Handle search query parameters
        search_query = request.args.get('search')
        location_filter = request.args.get('location_filter')

        # Build the query based on the search criteria
        query = Venue.query
        if search_query:
            query = query.filter(or_(
                Venue.name.ilike(f'%{search_query}%'),
                Venue.place.ilike(f'%{search_query}%')
            ))
        if location_filter:
            query = query.filter(Venue.place.ilike(f'%{location_filter}%'))

        venues = query.all()
        if venues:
            return {'venues': [venue.to_dict() for venue in venues]}, 200
        else:
            return {'message': 'Venue not found'}, 404

    

    @jwt_required()
    #@cache.memoize(50)
    def post(self):
        #current_user = get_current_user()
        admin = Admin.query.get(get_jwt_identity())
        if not admin:
            return {'message': 'Admin not found'}, 404

        name = request.json.get('name')
        place = request.json.get('place')
        capacity = request.json.get('capacity')

        if not name or not place or not capacity:
            return {'message': 'Name, place, and capacity are required'}, 400

        venue = Venue(name=name, place=place, capacity=capacity, admin_id=admin.id)
        db.session.add(venue)
        db.session.commit()

        return {'message': 'Venue added successfully'}, 201

    @jwt_required()
    def put(self, venue_id):
        #current_user = get_current_user()
        admin = Admin.query.get(get_jwt_identity())
        if not admin:
            return {'message': 'Admin not found'}, 404

        venue = Venue.query.get(venue_id)
        if not venue:
            return {'message': 'Venue not found'}, 404

        name = request.json.get('name')
        place = request.json.get('place')
        capacity = request.json.get('capacity')
        print(name,place,capacity)
        if name:
            venue.name = name
            db.session.commit()
        if place:
            venue.place = place
            db.session.commit()
        if capacity:
            venue.capacity = capacity
            print(venue.capacity)
            db.session.commit()

        
        db.session.commit()

        return {'message': 'Venue updated successfully'}, 200

    @jwt_required()
    def delete(self, venue_id):
        #current_user = get_current_user()
        admin = Admin.query.get(get_jwt_identity())
        if not admin:
            return {'message': 'Admin not found'}, 404

        venue = Venue.query.get(venue_id)
        if not venue:
            return {'message': 'Venue not found'}, 404
        
        current_session = db.session.object_session(venue)
        if current_session is not None and current_session != db.session:
            # Detach the booking from the old session
            current_session.expunge(venue)

        db.session.delete(venue)
        db.session.commit()

        return {'message': 'Venue deleted successfully'}, 200



class ShowResource(Resource):
    @jwt_required()
    # @cache.memoize(50)
    def get(self, venue_id=None, show_id=None):
        admin = Admin.query.get(get_jwt_identity())
        venue = None
        if venue_id:
            venue = Venue.query.get(venue_id)
            if not venue:
                return {'message': 'Venue not found'}, 404

            shows = db.session.query(Show, Venue.name).join(Venue).filter(Show.venue_id == venue.id, Venue.admin_id == admin.id).all()
            return {'shows': [show.to_dict() for show ,venue_name in shows],'venue':venue.to_dict()}
        elif show_id:
            show=Show.query.get(show_id)
            return{'show':show.to_dict()}

        else:
            shows=Show.query.all()

        if shows:
            show_data = [show.to_dict() for show in shows]
            if venue:
               return {'shows': show_data,'venue':venue.to_dict()}
            else:
                return {'shows': show_data}    

        # if shows or venue:
        #     # return {'shows': [show.to_dict() for show ,venue_name in shows],'venue':venue.to_dict()}
        #     return {'shows': [show.to_dict() for show in shows], 'venue': venue.to_dict()}

        else:
            return {'message': 'Show_not_found'}

    


    """for show in shows:
    'name' = show.name,
    'rating'=show.rating, 
    'tags'=show.tags,           
    'ticket_price'=show.ticket_price,            
    'date'=show.date,        
    'time'=show.time,            
    'available_tickets'=show.available_tickets"""
    
        

    @jwt_required()
    def post(self, venue_id):
        admin = Admin.query.get(get_jwt_identity())
        if not admin:
            return{'message':'Admin not found'}, 404
        
        venue = Venue.query.filter_by(id=venue_id).first()
        #admin = Admin.query.filter_by(id=current_user.id).first()
        username = admin.username
        name = request.json.get('name')
        rating = request.json.get('rating')
        tags = request.json.get('tags')
        ticket_price = request.json.get('ticket_price')
        date = request.json.get('date')
        time = request.json.get('time')
        available_tickets = request.json.get('available_tickets')

        if not name or not ticket_price or not date or not time  or not available_tickets:
            return {'message': 'Name, ticket price, date, time, number of tickets are required'}, 400
        admin_id = admin.id
        venue_name = venue.name

        show = Show(name=name, rating=rating, tags=tags, ticket_price=ticket_price, available_tickets=available_tickets, date=date, time=time, venue_id=venue.id, admin_id=admin_id) 
        db.session.add(show)
        db.session.commit()
        return {'message': 'Show added successfully'}, 201
        

    @jwt_required()
    def put(self,show_id, venue_id=None):
        # db = SQLAlchemy(app)
        admin = Admin.query.get(get_jwt_identity())
        if not admin:
            return {'message': 'Admin not found'}, 404

        show = Show.query.filter_by(id=show_id).first()
        print(show)
        print(type(show))
        # breakpoint()
        print(show.id,show.name)
        # venue=Venue.query.get(show_id)
        # print("")
        if not show:
            return {'message': 'Show not found'}, 404
        
        if venue_id:
            venue = Venue.query.get(venue_id)
        if not venue:
            return {'message': 'Venue not found'}, 404
        
        #show = Show.query.filter_by(id=show_id).first()
        username = admin.username
        name = request.json.get('name')
        rating = request.json.get('rating')
        tags = request.json.get('tags')
        ticket_price = request.json.get('ticket_price')
        date = request.json.get('date')
        time = request.json.get('time')
        available_tickets = request.json.get('available_tickets')
            #show.venue_id = request.form.get("venue_id", show.venue_id)
        if name:
            show.name = name
            # print("vhjhjhj")
            # db.session.commit()
        if rating:
            show.rating=rating
        if tags:
            show.tags=tags
        if ticket_price:
            show.ticket_price=ticket_price
        if date:
            show.date=date
        if time:
            show.time=time
        if available_tickets:
            show.available_tickets=int(available_tickets)
        print(request.json)    
        print(rating,available_tickets)
        # db.session.merge(show)
        db.session.commit()
        # print(dir(show))
        
        return {'message': 'Show updated successfully'}, 200


    @jwt_required()
    def delete(self, show_id):
        admin = Admin.query.get(get_jwt_identity())
        if not admin:
            return {'message': 'Admin not found'}, 404

        show = Show.query.get(show_id)
        if not show:
            return {'message': 'Show not found'}, 404

        current_session = db.session.object_session(show)
        if current_session is not None and current_session != db.session:
            # Detach the booking from the old session
            current_session.expunge(show)
            
        db.session.delete(show)
        db.session.commit()

        return {'message': 'Show deleted successfully'}, 200



class BookingFormResource(Resource):
    @jwt_required()
    # @cache.memoize(50)
    def get(self, show_id):
        user = User.query.get(get_jwt_identity())
        if not user:
            return {'message': 'Please log in'}, 401

        show = Show.query.filter_by(id=show_id).first()
        # user = current_user.username
        return {'show': show.to_dict(),'user':user.to_dict()}, 200
        
            
    @jwt_required()
    def post(self, show_id):
        user = User.query.get(get_jwt_identity())
        if not user:
            return {'message': 'Please log in'}, 401
        
        show = Show.query.filter_by(id=show_id).first()
        num_tickets = request.json.get('num_tickets')
        ticket_price = show.ticket_price
        total_price = num_tickets * ticket_price
        booking_time = datetime.datetime.now()
        user_id = user.id
        username = user.username
        booking = Booking(num_tickets=num_tickets, total_price=total_price, show_id=show.id, booking_time=booking_time, user_id=user_id)

        show.available_tickets = show.available_tickets - num_tickets
        db.session.add(booking)
        db.session.commit()
        return {'message':'Booking made successfully','booking': booking.to_dict()}, 200

class BookingsResource(Resource):
    @jwt_required()
    def get(self, user_id,booking_id=None):
        user = User.query.get(get_jwt_identity())
        if not user:
            return {'message': 'Please log in'}, 401

        if booking_id:
            user_id = user_id  # Replace this with the actual user ID
            booking_id = booking_id  # Replace this with the actual booking ID

            # Query the database to fetch the booking with the given booking_id and user_id
            booking = Booking.query\
                .join(Show)\
                .join(Venue)\
                .join(User)\
                .filter(Booking.id == booking_id, User.id == user_id)\
                .with_entities(
                    Booking.id,
                    Booking.num_tickets,
                    Booking.total_price,
                    Show.id.label('show_id'),
                    Show.name.label('show_name'),
                    Booking.booking_time,
                    User.id.label('user_id'),
                    Venue.name.label('venue_name'),
                    Show.date.label('show_date'),
                    Show.time.label('show_time')
                )\
                .first()
            
            if booking:
                return ({
                        'booking': {  
                                        'bookingId': booking.id,
                                        'num_tickets': booking.num_tickets,
                                        'total_price': booking.total_price,
                                        'show_id':booking.show_id,
                                        'show_name': booking.show_name,
                                        'booking_time': booking.booking_time,
                                        'user_id': booking.user_id,
                                        'venue_name': booking.venue_name,
                                        'show_date': booking.show_date,
                                        'show_time': booking.show_time
                                    },
                        'user': user.to_dict()            
                    })

            else:
                return jsonify({'message': 'Booking not found',
                                'user': user.to_dict()})
        
        user_id = user.id
        bookings = Booking.query.join(Show).join(Venue).join(User).filter_by(id=user_id).with_entities(
            Booking.id,  # Include the id column
            Booking.num_tickets,
            Booking.total_price,
            Show.id.label('show_id'),
            Show.name.label('show_name'),
            Booking.booking_time,
            User.id.label('user_id'),
            Venue.name.label('venue_name'),
            Show.date.label('show_date'),
            Show.time.label('show_time')
        ).all()
        # bookings = Booking.query.join(Show).join(Venue).join(User).filter_by(id=user_id).with_entities(Booking.num_tickets, Booking.total_price, Show.name.label('show_name'), Booking.booking_time, User.id.label('user_id'), Venue.name.label('venue_name'), Show.date.label('show_date'), Show.time.label('show_time')).all()
        user = User.query.filter_by(id=user_id).first()
        print(bookings)

        # booking_time_str = bookings.booking_time.isoformat()
        
        if bookings:
            return ({
            'bookings': [{  
                            'bookingId': booking.id,
                            'num_tickets': booking.num_tickets,
                            'total_price': booking.total_price,
                            'show_id':booking.show_id,
                            'show_name': booking.show_name,
                            'booking_time': booking.booking_time,
                            'user_id': booking.user_id,
                            'venue_name': booking.venue_name,
                            'show_date': booking.show_date,
                            'show_time': booking.show_time
                        } for booking in bookings],
            'user': user.to_dict()            
        })
        else:
            return jsonify({'message': 'Booking not found',
                            'user': user.to_dict()})
        
    # @jwt_required()
    # def delete(self, bookingId):
    #     user = User.query.get(get_jwt_identity())
    #     if not user:
    #         return {'message': 'Please log in'}, 401

    #     booking = Booking.query.get(bookingId)
    #     if not booking:
    #         return {'message': 'Booking not found'}, 404

    #     if booking.user_id != user.id:
    #         return {'message': 'Unauthorized'}, 403

    #     show = booking.show
    #     show.available_tickets += booking.num_tickets
    #     db.session.commit()

    #     # Add cancellation logic here
    #     # Example: Set booking status to cancelled or delete the booking from the database
    #     db.session.delete(booking)
    #     db.session.commit()

    #     return {'message': 'Booking cancelled'}

    @jwt_required()
    def delete(self, bookingId):
        user = User.query.get(get_jwt_identity())
        if not user:
            return {'message': 'Please log in'}, 401

        booking = Booking.query.get(bookingId)
        if not booking:
            return {'message': 'Booking not found'}, 404

        if booking.user_id != user.id:
            return {'message': 'Unauthorized'}, 403

        show = booking.show
        show.available_tickets += booking.num_tickets
        db.session.commit()

        # Check if the booking is attached to the current session
        current_session = db.session.object_session(booking)
        if current_session is not None and current_session != db.session:
            # Detach the booking from the old session
            current_session.expunge(booking)

        # Delete the booking from the current session
        db.session.delete(booking)
        db.session.commit()

        return {'message': 'Booking cancelled'}


        

        


api.add_resource(Home,'/')
api.add_resource(SignupResource, '/signup')
api.add_resource(AdminLoginResource,'/admin_login','/profile/<int:admin_id>','/delete_admin/<int:admin_id>')
api.add_resource(UserLoginResource,'/user_login','/user_profile/<int:user_id>','/delete_user/<int:user_id>')
api.add_resource(VenueResource, '/venues', '/venues/<int:venue_id>','/venue_mgt','/venue_mgt/delete/<int:venue_id>','/add_venue','/edit_venue/<int:venue_id>','/venue_mgt/<int:venue_id>')
api.add_resource(ShowResource, '/shows', '/shows/<int:venue_id>','/show_mgt/<int:venue_id>','/edit_show/<int:show_id>','/edit_show/<int:venue_id>/<int:show_id>','/show_mgt_venue/delete/<int:show_id>','/show_mgt/<int:venue_id>','/add_show/<int:venue_id>')
api.add_resource(BookingFormResource, '/booking_form/<int:show_id>')
api.add_resource(BookingsResource, '/bookings/<int:user_id>','/bookings/delete/<int:bookingId>', '/bookings/<int:user_id>/<int:booking_id>')


@app.route("/<int:admin_id>/<int:venue_id>/venue_details/download/",methods=["GET"])
@jwt_required()
# @cache.memoize(timeout=25)  # So that the user doesn't spam the download button
def venueDetailsDownload(venue_id,admin_id):
    
    print(venue_id)
    admin=Admin.query.get(admin_id)
    print(admin)
    username = admin.username
    print(username)
    
    # print(username)
    return_msg=download_venueDetails(venue_id, username)
    print(return_msg)
    
    return {'msg': "Done"}, 200

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

@celery.task(name="monthly_report")
def monthly_report():
    # last_month=(datetime.now()).month-1
    now = datetime.datetime.now()
    month = now.strftime('%B')
    year = now.strftime('%Y')
    today = date_today().strftime('%Y-%m-%d')
    with app.app_context():
        users=User.query.all()
    print(users)
    with open(r"templates/report_mail_temp.html") as file:
        msg_temp = Template(file.read())

    with open(r"templates/report.html") as file:
        pdf_temp = Template(file.read())

    done_users = []
    for user_obj in users:
        user = user_obj.username
        print(user)
        user_obj_bookings=Booking.query.filter_by(user_id=user_obj.id)
        print(user_obj_bookings)
        account_details = accountDetails(user_obj,user_obj_bookings)  # Function returns all required account details
        bookings = bookingDetails(user_obj,user_obj_bookings)  
        
        message = msg_temp.render(user=user)
        print("r15")
        pdf_html = pdf_temp.render(today=str(today),
                                month=month,
                                account_details=account_details,
                                bookings=bookings,
                                
                                username=user
                                )
        with open('xyz.html','w') as file:
            file.write(pdf_html)
        # breakpoint()
        
        sub = f"[MONTHLY REPORT] Ticketocks"
        if user not in done_users:
            # print("r17.0")
            pdf_path = generate_pdf(usr=user, template='xyz.html')
            # print("r17.1")
            send_email(to_address=user_obj.email, subject=sub, message=message, attachment=pdf_path)
            # print("r17.2")
            done_users.append(user)
        # print("r18")

        print(f"------MONTHLY REPORT SENT FOR {user}---------")
    return("report sent")
    

@celery.task(name="webhook")
def webhook_chat():
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    data = {'text': 'Reminder: Please visit/book something.'}

    res = http_obj.request('https://chat.googleapis.com/v1/spaces/AAAAOZ2wYkA/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Xnld14KF22pyg4Evuyo-xbLYhZ4ZZlW4MVvz75M-MkY', 
                           method='POST', headers=message_headers, body=dumps(data))
    print("Reminder sent. Response:", res)


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


@cache.memoize(timeout=120)
def export_venue_to_csv(venue):
    filename = "venue_" + current_timestamp() + ".csv"
    filepath = f"static/venue_detailsDownload/{filename}"
    with open(filepath, 'w', newline='') as venue_file:
        fieldnames = ['venue_id', 'venue_name', 'venue_place', 'venue_capacity']
        csv_writer = csv.DictWriter(venue_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerow({
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_place': venue.place,
            'venue_capacity': venue.capacity,
        })

    return filepath

# @celery.task
# @celery_inst.task()
@cache.memoize(timeout=25)  # So that the user doesn't spam the download button
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
            filepath = export_venue_to_csv(venue)
            with open(r"templates/download_ready.html") as file:
                temp = Template(file.read())
            sub = "[Venue Details DOWNLOAD READY] Ticketocks"
            message = temp.render(user=username,venue=venue.name, file_type="Venue data")
            print(message)
            send_email(to_address=to_email, subject=sub, message=message, attachment=filepath)
            alert("Mail sent successfully!", "success")

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
    # print("er0")
    mail=MIMEMultipart()
    mail["From"]=SENDER_ADDRESS
    mail["To"]=to_address
    mail["Subject"]=subject
    # print("er1")
    mail.attach(MIMEText(message, "html"))
    print("er2")

    if attachment is not None:
        # print("er2.1")
        with open(attachment, "rb") as attachment_file:
            # print("er2.2")
            part = MIMEBase("application", "octet-stream")
            # print("er2.3")
            part.set_payload(attachment_file.read())
            # print("er2.4")
            encoders.encode_base64(part)
            # print("er2.5")
            part.add_header("Content-Disposition", f"attachment; filename={attachment[len('static/venue_detailsDownload/'):]}")
            mail.attach(part)
            # print("er3")
    # print("er4")
    s=smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    # print("er4.1")
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    # print("er4.2")
    s.send_message(mail)
    # print("er4.3")
    s.quit()
    # print("er4")
    if attachment is not None:
        abs_attachment_path = os.path.abspath(attachment)
        os.remove(abs_attachment_path)
    # print("er5")
    return True
    

if __name__=="__main__":
  
    app.debug=True
    app.run(port=8001)
