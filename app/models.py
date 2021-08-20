import jwt

from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


class DictMixin(object):
  def toDict(self):
    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class BaseMixin(DictMixin):
  created = db.Column(db.DateTime, default=datetime.utcnow)
  updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


blogger_trip = db.Table('blogger_trip',
  db.Column('blogger_id', db.Integer, db.ForeignKey('blogger.id'),
    primary_key=True),
  db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'),
    primary_key=True)
)

blogger_post = db.Table('blogger_post',
  db.Column('blogger_id', db.Integer, db.ForeignKey('blogger.id'),
    primary_key=True),
  db.Column('post_id', db.Integer, db.ForeignKey('post.id'),
    primary_key=True)
)

post_trip = db.Table('post_trip',
  db.Column('post_id', db.Integer, db.ForeignKey('post.id'),
    primary_key=True),
  db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'),
    primary_key=True)
)

hashtag_trip = db.Table('hashtag_trip',
  db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id'),
    primary_key=True),
  db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'),
    primary_key=True)
)

hashtag_post = db.Table('hashtag_post',
  db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id'),
    primary_key=True),
  db.Column('post_id', db.Integer, db.ForeignKey('post.id'),
    primary_key=True)
)

class Blogger(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(40), unique=True)
  full_name = db.Column(db.String(128))
  followers = db.Column(db.Integer)
  count_likes = db.Column(db.Integer)
  count_comments = db.Column(db.Integer)
  count_posts = db.Column(db.Integer)
  er = db.Column(db.Float)
  public = db.Column(db.Boolean)
  verify = db.Column(db.Boolean)
  Posts = db.relationship('Post', back_populates='Blogger')


class Trip(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
  invitation_id = db.Column(db.Integer, db.ForeignKey('invitation_info.id'))
  name = db.Column(db.String(40), unique=True)
  date = db.Column(db.DateTime)
  Invitation = db.relationship('InvitationInfo', back_populates='Trips')
  Bloggers = db.relationship('Blogger', secondary=blogger_trip,
    backref=db.backref('Trips'))
  Hashtags = db.relationship('Hashtag', secondary=hashtag_trip,
    backref=db.backref('Trips'))
  Posts = db.relationship('Post', secondary=post_trip,
    backref=db.backref('Trips'))
  Route = db.relationship('Route', back_populates='Trips')


class StatusTrip(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(40), unique=True)
  label = db.Column(db.String(40), unique=True)

class InvitationInfo(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  label = db.Column(db.String(500), unique=True)
  Trips = db.relationship('Trip', back_populates='Invitation')

class TypeMedia(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  label = db.Column(db.String(40), unique=True)

class Route(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(40), unique=True)
  RoutePlaces = db.relationship('RoutePlace', back_populates='Route')
  Trips = db.relationship('Trip', back_populates='Route')

class RoutePlace(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  order = db.Column(db.Integer)
  place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
  route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
  Place = db.relationship('Place', back_populates='RoutePlaces')
  Route = db.relationship('Route', back_populates='RoutePlaces')


class Hashtag(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(40), unique=True)


class Settings(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  key = db.Column(db.String(40), unique=True)
  value = db.Column(db.String(100), unique=True)


class Media(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(40), unique=True)
  type = db.Column(db.String(100), unique=True)
  src = db.Column(db.String(100), unique=True)


class Place(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  lat = db.Column(db.Float)
  lon = db.Column(db.Float)
  RoutePlaces = db.relationship('RoutePlace', back_populates='Place')


class User(DictMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  login = db.Column(db.String(40), unique=True)
  pass_hash = db.Column(db.String(128))
  registered = db.Column(db.DateTime, nullable=False)
  updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

  def __init__(self):
    self.registered = datetime.now()

  def set_password(self, password):
    self.pass_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pass_hash, password)

class Post(db.Model, DictMixin):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  blogger_id = db.Column(db.Integer, db.ForeignKey('blogger.id'))
  name = db.Column(db.String(200))
  date = db.Column(db.DateTime)
  count_likes = db.Column(db.Integer)
  count_comments = db.Column(db.Integer)
  deleted = db.Column(db.Boolean)
  audience_coverage = db.Column(db.Integer)
  Blogger = db.relationship('Blogger', back_populates='Posts')

