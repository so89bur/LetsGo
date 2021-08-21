import json

from flask import request

from app import app, db
from app.utils import send_datetime_to_client
from app.api import support
from app.models import Place


def prepare_place(instance):
  return {
    'id': instance.id,
    'name': instance.name,
    'lat': instance.lat,
    'lon': instance.lon,
    'routes_count': len(instance.RoutePlaces),
  }


@support
@app.route('/api/v1/place', methods=['POST'])
def new_place():
  data = prepare_form_data(request.form)
  instance = Place()
  db.session.add(instance)
  for property_name, property_value in data.items():
    if property_value:
      setattr(instance, property_name, property_value)
  db.session.add(instance)
  db.session.commit()
  return json.dumps({'success': True})


@support
@app.route('/api/v1/place/<id>', methods=['GET'])
def get_place(id):
  result = None
  instance = Place.query.filter_by(id=id).first()
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
@app.route('/api/v1/places', methods=['GET'])
def get_palces():
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
    query = Place.query.filter(Place.name.ilike(search_value))
  elif filter_value and filter_prop:
    query = Place.query.filter(getattr(Place, filter_prop) == filter_value)
  else:
    query = Place.query
  if order_type == 'asc':
    order_info = getattr(Place, order_by).asc()
  else:
    order_info = getattr(Place, order_by).desc()
  for item in query.order_by(order_info).slice(start, start + limit).all():
    items.append(prepare_place(item))
  return json.dumps({
    'success': True,
    'total': Place.query.count(),
    'result': items
  })


@support
@app.route('/api/v1/place/<id>', methods=['PUT'])
def edit_place(id):
  data = prepare_form_data(request.form)
  if id:
    instance = Place.query.filter_by(id=id).first()
    for property_name, property_value in data.items():
      if property_value:
        instance[property_name] = property_value
    db.session.add(instance)
    db.session.commit()
    return json.dumps({'success': True})
  else:
    return json.dumps({'success': False})


@support
@app.route('/api/v1/place/<id>', methods=['DELETE'])
def remove_place(id):
  if id:
    Place.query.filter_by(id=id).first().delete()
    db.session.commit()
    return json.dumps({'success': True})
  else:
    return json.dumps({'success': False})
