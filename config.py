import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  CSRF_ENABLED = True
  WTF_CSRF_SECRET_KEY = 'dsofpkoasodksap'
  SQLALCHEMY_DATABASE_URI = 'postgresql://admin:superpassword@localhost:5432/posteach'
  CACHE_TYPE = "simple"
  CACHE_DEFAULT_TIMEOUT = 300
  MAX_CONTENT_LENGTH = 16 * 1024 * 1024
  ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
  DEBUG = False

class DevelopConfig(Config):
  DEBUG = True
  ASSETS_DEBUG = True
