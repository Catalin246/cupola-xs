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

ml_model_wifi = load_model('wifidata_model.h5')

ml_model_cinema = load_model('cinemadata_model.h5')

def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    # Enable CORS
    CORS(app)
    
    return app
