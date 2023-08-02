from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Creating a database variable to communicate with the database file! Using SQLAlchemy ORM for it
db = SQLAlchemy()

class Admin(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(128), nullable=True)
    password_hash = db.Column(db.String(128))
    email=db.Column(db.String(80),nullable=False)
    venues=db.relationship('Venue',backref='admin', cascade='all, delete-orphan')
    shows=db.relationship('Show',backref='admin', cascade='all, delete-orphan')

    def delete(self):
        for venue in self.venues:
            db.session.delete(venue)
        for show in self.shows:
            db.session.delete(show)
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(128), nullable=True)
    password_hash = db.Column(db.String(128))
    email=db.Column(db.String(80),nullable=False)
    bookings=db.relationship('Booking', backref='booking_id', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.username,
            'email': self.email
       }


    def delete(self):
        for booking in self.bookings:
            db.session.delete(booking)
        db.session.delete(self)
        db.session.commit()

    def is_admin(self):
        admin = Admin.query.filter_by(username=self.username, email=self.email).first()
        if admin:
            return True
        else:
            return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Venue(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    place = db.Column(db.String(80), nullable=False)
    capacity= db.Column(db.Integer, nullable=False)
    shows=db.relationship('Show',backref='show_name')
    admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'),nullable=False,)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'place': self.place,
            'capacity': self.capacity,
            'admin_id': self.admin_id
       }


class Show(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    rating= db.Column(db.REAL, nullable=False)
    tags= db.Column(db.String, nullable=False)
    ticket_price= db.Column(db.REAL, nullable=False)
    available_tickets= db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    venue_id= db.Column(db.Integer ,db.ForeignKey('venue.id',ondelete='CASCADE'), nullable=False)
    admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'),nullable=False)
    #bookings = db.relationship('Booking', backref='shows', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rating': self.rating,
            'tags': self.tags,
            'ticket_price': self.ticket_price,
            'available_tickets': self.available_tickets,
            'date': self.date,
            'time': self.time,
            'venue_id': self.venue_id,
            'admin_id': self.admin_id
        }


class Booking(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    # booking_time = db.Column(db.String, default=datetime.utcnow)
    booking_time = db.Column(db.String)

    total_price=db.Column(db.REAL, nullable=False)

    user = db.relationship('User', backref='booking')
    show = db.relationship('Show', backref='booking')

    def to_dict(self):
        return{
            'num_tickets': self.num_tickets,
            'total_price': self.total_price,
            'show_name': self.show.name,
            'booking_time': self.booking_time,
            'user_id': self.user.id,
            # 'venue_name': self.venue.name,
            'show_date': self.show.date,
            'show_time': self.show.time
        }
