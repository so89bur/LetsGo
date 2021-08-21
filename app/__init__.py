from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

ATTEMPTS_NUMBER = 10

app = Flask(__name__,
            static_folder="../../static",
            template_folder=".",
            )

CORS(app, resources={r"*": {"origins": "*"}})

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, api
