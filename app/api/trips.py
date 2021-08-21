import json

from flask import request

from app import app, db
from app.utils import send_datetime_to_client
from app.api import support
from app.models import Trip, Blogger, Post, Hashtag


def prepare_trip(instance):
  prepared_posts = []
  prepared_hashtags = []
  prepared_bloggers = []
  for blogger in instance.Bloggers:
    prepared_bloggers.append({
      'id': blogger.id,
      'username': blogger.username,
      'full_name': blogger.full_name,
      'followers': blogger.followers,
      'profile_pic_url': blogger.profile_pic_url,
      'is_business_account': blogger.is_business_account,
    })
  for hashtag in instance.Hashtags:
    prepared_hashtags.append({
      'id': blogger.id,
      'name': hashtag.name,
    })
  for post in instance.Posts:
    prepared_posts.append({
      'id': post.id,
      'name': post.name,
    })
  prepared_route = None
  if instance.Route:
    prepared_route = {
      'id': instance.Route.id,
      'name': instance.Route.name,
    }
  return {
    'id': instance.id,
    'name': instance.name,
    'date': send_datetime_to_client(instance.date),
    'invitation_text': instance.invitation_text,
    'Bloggers': prepared_bloggers,
    'Posts': prepared_posts,
    'Hashtags': prepared_hashtags,
    'Route': prepared_route,
  }


@support
@app.route('/api/v1/trip/attach/blogger', methods=['POST'])
def attach_blogger():
  data = json.loads(request.data)
  trip_id = data.get('trip_id', None)
  blogger_id = data.get('blogger_id', None)
  trip = Trip.query.filter_by(id=trip_id).first()
  exists_bloggers_ids = []
  if trip:
    for blogger in trip.Bloggers:
      if blogger.id not in exists_bloggers_ids:
        exists_bloggers_ids.append(blogger.id)
    if blogger_id not in exists_bloggers_ids:
      new_blogger = Blogger.query.filter_by(id=blogger_id).first()
      if new_blogger:
        trip.Bloggers.append(new_blogger)
  db.session.commit()
  return json.dumps({'success': True})

@support
@app.route('/api/v1/trip/detach/blogger', methods=['POST'])
def detach_blogger():
  data = json.loads(request.data)
  trip_id = data.get('trip_id', None)
  blogger_id = data.get('blogger_id', None)
  trip = Trip.query.filter_by(id=trip_id).first()
  exists_bloggers = []
  if trip:
    for blogger in trip.Bloggers:
      if blogger.id != blogger_id:
        exists_bloggers.append(blogger)
    trip.Bloggers = exists_bloggers
  db.session.commit()
  return json.dumps({'success': True})

@support
@app.route('/api/v1/trip', methods=['POST'])
def new_trip():
  data = prepare_form_data(request.form)
  instance = Trip()
  db.session.add(instance)
  for property_name, property_value in data.items():
    if property_value:
      setattr(instance, property_name, property_value)
  db.session.add(instance)
  db.session.commit()
  return json.dumps({'success': True})


@support
@app.route('/api/v1/trip/<id>', methods=['GET'])
def get_trip(id):
  result = None
  instance = Trip.query.filter_by(id=id).first()
  if instance:
    result = prepare_trip(instance)
  if result:
    return json.dumps({
      'success': True,
      'result': result
    })
  else:
    return json.dumps({'success': False})


@support
@app.route('/api/v1/trips', methods=['GET'])
def get_trips():
  start = request.args.get('start', default=0, type=int)
  limit = request.args.get('limit', default=20, type=int)
  order_by = request.args.get('order_by', default='id', type=str)
  order_type = request.args.get('order_type', default='asc', type=str)
  filter_prop = request.args.get('filter_prop', default='name')
  filter_value = request.args.get('filter_value', default=None)
  search_query = request.args.get('search_query', default=None)
  items = []
  if search_query:
    search_value = '%{}%'.format(search_query).lower()
    query = Trip.query.filter(Trip.name.ilike(search_value))
  elif filter_value and filter_prop:
    query = Trip.query.filter(getattr(Trip, filter_prop) == filter_value)
  else:
    query = Trip.query
  if order_type == 'asc':
    order_info = getattr(Trip, order_by).asc()
  else:
    order_info = getattr(Trip, order_by).desc()
  for item in query.order_by(order_info).slice(start, start + limit).all():
    items.append(prepare_trip(item))
  return json.dumps({
    'success': True,
    'total': Trip.query.count(),
    'result': items
  })


@support
@app.route('/api/v1/trip/<id>', methods=['PUT'])
def edit_trip(id):
  data = prepare_form_data(request.form)
  if id:
    instance = Trip.query.filter_by(id=id).first()
    for property_name, property_value in data.items():
      if property_value:
        instance[property_name] = property_value
    db.session.add(instance)
    db.session.commit()
    return json.dumps({'success': True})
  else:
    return json.dumps({'success': False})


@support
@app.route('/api/v1/trip/<id>', methods=['DELETE'])
def remove_trip(id):
  if id:
    Trip.query.filter_by(id=id).first().delete()
    db.session.commit()
    return json.dumps({'success': True})
  else:
    return json.dumps({'success': False})
