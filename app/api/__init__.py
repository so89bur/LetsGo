import json

from flask import request
from functools import wraps

from app import db
from app.models import User


def support(func):
  def func_wrapper(*args, **kwargs):
    try:
      for i in range(ATTEMPTS_NUMBER):
        try:
          return func(*args, **kwargs)
        except Exception:
          continue
        break
    except Exception as e:
      db.session.rollback()
      return json.dumps({'success': False})
    finally:
      db and db.close()
    return func_wrapper

from . import trips
