from flask import Flask, abort, render_template,url_for,request,redirect,flash, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager,login_required, login_user, logout_user, current_user
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt,get_jwt_identity
#from sqlalchemy.orm import relationship
from datetime import datetime
#from models import db, User, Post, Authentication
from flask_restful import Resource, reqparse,Api
from flask import jsonify, make_response
from flask_cors import CORS
from celery_worker import *
from celery_tasks import *
from models import *
# from cache_instance import current_cache_inst as cache
from jinja2 import Template
# from flask_caching import Cache


#app.app_context().push()
#app.app_context()
# with app.app_context():
#     users = User.query.all()
#     print(users)




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'secret-key'
api = Api(app)
CORS(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate=Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.app_context().push()

# app.config.update(
#     CACHE_TYPE= 'RedisCache',
#     CACHE_REDIS_HOST='localhost',
#     CACHE_REDIS_PORT=6379
#     )

# app.config.update(CELERY_CONFIG={
#     'broker_url': 'redis://localhost:6379/1',
#     'result_backend': 'redis://localhost:6379/1',
#     'timezone': 'Asia/Kolkata'
# })

# app.config['broker_url'] = 'redis://localhost:6379/0'
# app.config['result_backend'] = 'redis://localhost:6379/1'

# cache=Cache(app)

#celery = make_celery(app)
# celery_inst = make_celery(app)
# app.app_context().push()

# @celery.task()
# def add_together(a, b):
#     return a + b

# class Admin(UserMixin,db.Model):
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password=db.Column(db.String(128), nullable=True)
#     password_hash = db.Column(db.String(128))
#     email=db.Column(db.String(80),nullable=False)
#     venues=db.relationship('Venue',backref='admin', cascade='all, delete-orphan')
#     shows=db.relationship('Show',backref='admin', cascade='all, delete-orphan')

#     def delete(self):
#         for venue in self.venues:
#             db.session.delete(venue)
#         for show in self.shows:
#             db.session.delete(show)
#         db.session.delete(self)
#         db.session.commit()

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# class User(UserMixin,db.Model):
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password=db.Column(db.String(128), nullable=True)
#     password_hash = db.Column(db.String(128))
#     email=db.Column(db.String(80),nullable=False)
#     bookings=db.relationship('Booking', backref='booking_id', cascade='all, delete-orphan')

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.username,
#             'email': self.email
#        }


#     def delete(self):
#         for booking in self.bookings:
#             db.session.delete(booking)
#         db.session.delete(self)
#         db.session.commit()

#     def is_admin(self):
#         admin = Admin.query.filter_by(username=self.username, email=self.email).first()
#         if admin:
#             return True
#         else:
#             return False

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# class Venue(UserMixin,db.Model):
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     name = db.Column(db.String(80), nullable=False)
#     place = db.Column(db.String(80), nullable=False)
#     capacity= db.Column(db.Integer, nullable=False)
#     shows=db.relationship('Show',backref='show_name')
#     admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'),nullable=False,)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'place': self.place,
#             'capacity': self.capacity,
#             'admin_id': self.admin_id
#        }


# class Show(UserMixin,db.Model):
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     name = db.Column(db.String(80), nullable=False)
#     rating= db.Column(db.REAL, nullable=False)
#     tags= db.Column(db.String, nullable=False)
#     ticket_price= db.Column(db.REAL, nullable=False)
#     available_tickets= db.Column(db.Integer, nullable=False)
#     date = db.Column(db.String, nullable=False)
#     time = db.Column(db.String, nullable=False)
#     venue_id= db.Column(db.Integer ,db.ForeignKey('venue.id',ondelete='CASCADE'), nullable=False)
#     admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'),nullable=False)
#     #bookings = db.relationship('Booking', backref='shows', lazy='dynamic')

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'rating': self.rating,
#             'tags': self.tags,
#             'ticket_price': self.ticket_price,
#             'available_tickets': self.available_tickets,
#             'date': self.date,
#             'time': self.time,
#             'venue_id': self.venue_id,
#             'admin_id': self.admin_id
#         }


# class Booking(UserMixin,db.Model):
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
#     num_tickets = db.Column(db.Integer, nullable=False)
#     # booking_time = db.Column(db.String, default=datetime.utcnow)
#     booking_time = db.Column(db.String)

#     total_price=db.Column(db.REAL, nullable=False)

#     user = db.relationship('User', backref='booking')
#     show = db.relationship('Show', backref='booking')

#     def to_dict(self):
#         return{
#             'num_tickets': self.num_tickets,
#             'total_price': self.total_price,
#             'show_name': self.show.name,
#             'booking_time': self.booking_time,
#             'user_id': self.user.id,
#             # 'venue_name': self.venue.name,
#             'show_date': self.show.date,
#             'show_time': self.show.time
#         }

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
        admin = User.query.get(admin_id)

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

        if name:
            venue.name = name
        if place:
            venue.place = place
        if capacity:
            venue.capacity = capacity

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
    def put(self, show_id):
        admin = Admin.query.get(get_jwt_identity())
        if not admin:
            return {'message': 'Admin not found'}, 404

        show = Show.query.get(show_id)
        if not show:
            return {'message': 'Show not found'}, 404
        
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
            show.available_tickets=available_tickets

        db.session.commit()
        
        return {'message': 'Show updated successfully'}, 200


    @jwt_required()
    def delete(self, show_id):
        admin = Admin.query.get(get_jwt_identity())
        if not admin:
            return {'message': 'Admin not found'}, 404

        show = Show.query.get(show_id)
        if not show:
            return {'message': 'Show not found'}, 404

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

        # Add cancellation logic here
        # Example: Set booking status to cancelled or delete the booking from the database
        db.session.delete(booking)
        db.session.commit()

        return {'message': 'Booking cancelled'}



        

        


api.add_resource(Home,'/')
api.add_resource(SignupResource, '/signup')
api.add_resource(AdminLoginResource,'/admin_login','/profile/<int:admin_id>','/delete_admin/<int:admin_id>')
api.add_resource(UserLoginResource,'/user_login','/user_profile/<int:user_id>','/delete_user/<int:user_id>')
api.add_resource(VenueResource, '/venues', '/venues/<int:venue_id>','/venue_mgt','/venue_mgt/delete/<int:venue_id>','/add_venue','/edit_venue/<int:venue_id>','/venue_mgt/<int:venue_id>')
api.add_resource(ShowResource, '/shows', '/shows/<int:venue_id>','/show_mgt/<int:venue_id>','/edit_show/<int:show_id>','/show_mgt_venue/delete/<int:show_id>','/show_mgt/<int:venue_id>','/add_show/<int:venue_id>')
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


    

if __name__=="__main__":
  
  app.debug=True
  app.run(port=8001)
