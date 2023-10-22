"""
This is where we'll perform the imports and object initializations. Doing it this way seems cleaner and avoids
circular imports, which was causing me problems in my early attempts at building out the models.
"""

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
from .events import socketio

socketio.init_app(app)
