from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os

import pickle

import tensorflow 
from tensorflow import keras
from tensorflow.keras.models import load_model

from .config import config_by_name
from dotenv import load_dotenv

load_dotenv()

wifi_model_path = os.getenv('WIFI_MODEL_PATH')
cinema_model_path = os.getenv('CINEMA_MODEL_PATH')

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

ml_model_wifi_hourly = load_model(wifi_model_path)

ml_model_cinema = load_model(cinema_model_path)

def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    # Enable CORS
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    
    return app
