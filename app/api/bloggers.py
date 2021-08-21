import json

from flask import request

from app import app, db
from app.utils import send_datetime_to_client
from app.api import support
from app.models import Trip, Blogger, Post, Hashtag


def prepare_blogger(instance):
  return {
    'id': instance.id,
    "username": instance.username,
    "full_name": instance.full_name,
    "count_likes": instance.count_likes,
    "count_comments": instance.count_comments,
    "count_posts": instance.count_posts,
    "followers": instance.followers,
    "er": instance.er,
    "is_business_account": instance.is_business_account,
    "verify": instance.verify,
    "profile_pic_url": instance.profile_pic_url,
  }


@support
@app.route('/api/v1/bloggers', methods=['GET'])
def get_bloggers():
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
    query = Blogger.query.filter(Blogger.name.ilike(search_value))
  elif filter_value and filter_prop:
    query = Blogger.query.filter(getattr(Blogger, filter_prop) == filter_value)
  else:
    query = Blogger.query
  if order_type == 'asc':
    order_info = getattr(Blogger, order_by).asc()
  else:
    order_info = getattr(Blogger, order_by).desc()
  for item in query.order_by(order_info).slice(start, start + limit).all():
    items.append(prepare_blogger(item))
  return json.dumps({
    'success': True,
    'total': Blogger.query.count(),
    'result': items
  })
