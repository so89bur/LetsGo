import json

from flask import request

from app import app, db
from app.utils import send_datetime_to_client
from app.api import support
from app.models import Settings


SETTINGS_KEYS = [
  'instagram_login',
  'instagram_password',
]


def get_settings_item(key, default=None):
  item = Settings.query.filter(Settings.key == key).first()
  if item is not None:
    return item.value
  else:
    return default


def save_settings_item(key, value):
  item = Settings.query.filter(Settings.key == key).first()
  if item is None:
    item = Settings(key=key)
  item.value = value
  db.session.add(item)
  db.session.commit()


@support
@app.route('/api/v1/settings', methods=['GET'])
def get_settings():
  data = {}
  for key in SETTINGS_KEYS:
    data[key] = get_settings_item(key, "")
  return json.dumps(data)


@support
@app.route('/api/v1/settings', methods=['POST'])
def set_settings():
  data = request.json
  for key in SETTINGS_KEYS:
    save_settings_item(key, data[key])
  return json.dumps({})
