from random import randint, choice

from datetime import datetime

from app import app, db
from app.models import Trip, Post, Blogger, Hashtag, TypeMedia, StatusTrip, \
  InvitationInfo

INVITATIONS = [
  'Хотим пригласить вас принять участие в травел-поездке'
]
TRIP_STATUSES = {
  'new': 'Новая',
  'inprogress': 'В процессе',
  'finished': 'Завершена',
}

HASHTAGS = ['травел_блогер', 'красивая_самара']

def clear_data():
  for key in data.keys():
    data[key].clear()

def create_random_point(x0, y0, distance):
  r = distance / 111300
  u = np.random.uniform(0, 1)
  v = np.random.uniform(0, 1)
  w = r * np.sqrt(u)
  t = 2 * np.pi * v
  x = w * np.cos(t)
  x1 = x / np.cos(y0)
  y = w * np.sin(t)
  return {
    lat: round(x0 + x1, 5),
    lon: round(y0 + y, 5),
  }

def write_hashtags():
  for name in HASHTAGS:
    trip = Hashtag(name=name)

def write_places():
  for index in range(100):
    place = Place()
    point = create_random_point(BASE_LAT, BASE_LONG, 100000)
    place.name = 'place {}'.format(index)
    place.lat = point['lat']
    place.lon = point['lon']
    db.session.add(place)
  db.session.commit()

def write_posts():
  for index in range(100):
    post = Post()
    post.name = 'Post {}'.format(index)
    post.date = datetime.now()
    post.count_likes = randint(5000, 10000)
    post.count_comments = randint(100, 5000)
    post.deleted = False
    post.audience_coverage = randint(0, 100)
    db.session.add(post)
  db.session.commit()

def write_bloggers():
  for index in range(20):
    blogger = Blogger()
    blogger.username = 'username_{}'.format(index)
    blogger.full_name = 'Пользователь {}'.format(index)
    blogger.followers = randint(1000, 500000)
    blogger.count_likes = randint(5000, 10000)
    blogger.count_comments = randint(100, 5000)
    blogger.count_posts = randint(100, 5000)
    blogger.er = randint(0, 20)
    blogger.public = bool(randint(0, 1))
    blogger.verify = bool(randint(0, 1))
    random_posts = []
    random_trips = []
    exist_posts = []
    for post_index in range(20):
      post = choice(Post.query.all())
      if post.id not in exist_posts:
        random_posts.append(post)
        exist_posts.append(post.id)
    exist_trips = []
    blogger.Posts = random_posts
    for trip_index in range(5):
      trip = choice(Trip.query.all())
      if trip.id not in exist_trips:
        random_trips.append(trip)
        exist_trips.append(trip.id)
    blogger.Posts = random_posts
    blogger.Trips = random_trips
    db.session.add(blogger)
  db.session.commit()

def write_trips():
  for index in range(20):
    trip = Trip()
    trip.name = 'Поздка {}'.format(index)
    trip.date = datetime.now()
    trip.Invitation = choice(InvitationInfo.query.all())
    db.session.add(trip)
  db.session.commit()

def write_base_data():
  for name in ['photo', 'video']:
    media = TypeMedia(label=name)
    db.session.add(media)
  db.session.commit()
  for name, label in TRIP_STATUSES.items():
    status = StatusTrip(name=name, label=label)
    db.session.add(status)
  for label in INVITATIONS:
    invitation = InvitationInfo(label=label)
    db.session.add(invitation)
  db.session.commit()


def reset_db():
  db.drop_all()
  db.create_all()


if __name__ == '__main__':
  reset_db()
  write_base_data()
  write_hashtags()
  write_posts()
  write_trips()
  write_bloggers()