import json

from flask import request

from app import app, db
from app.utils import send_datetime_to_client
from app.api import support
from app.models import Trip, Blogger, Post, Hashtag


def prepare_hashtag(instance):
  return {
    'id': instance.id,
    "name": instance.name,
    "trips_count": len(instance.Trips),
    "posts_count": len(instance.Posts)
  }


@support
@app.route('/api/v1/hashtags', methods=['GET'])
def get_hashtags():
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
    query = Hashtag.query.filter(Hashtag.name.ilike(search_value))
  elif filter_value and filter_prop:
    query = Hashtag.query.filter(getattr(Hashtag, filter_prop) == filter_value)
  else:
    query = Hashtag.query
  if order_type == 'asc':
    order_info = getattr(Hashtag, order_by).asc()
  else:
    order_info = getattr(Hashtag, order_by).desc()
  for item in query.order_by(order_info).slice(start, start + limit).all():
    items.append(prepare_hashtag(item))
  return json.dumps({
    'success': True,
    'total': Hashtag.query.count(),
    'result': items
  })
