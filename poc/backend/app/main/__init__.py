from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

import pickle

import tensorflow 
from tensorflow import keras
from tensorflow.keras.models import load_model

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

ml_model_wifi_hourly = load_model('models/wifi/wifidata_model_20240619_233511.h5')

ml_model_cinema = load_model('models/cinema/cinemadata_model_20240619_233538.h5')

def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    # Enable CORS
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    
    return app
