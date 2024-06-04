from app.main import ml_model_wifi, scaler_wifi, ml_model_cinema, scaler_cinema

from app.main.service.wifi_data_service import get_all_wifi_data

from flask import jsonify

from typing import Dict, Tuple
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

def predict_wifi_data() :
    
    wifi_data = get_all_wifi_data()

    wifi_devices_values = []

    for data in wifi_data:
        wifi_devices_values.append(data.total_online_devices)

    X = []

    seq_length = 7

    for i in range(len(wifi_devices_values) - seq_length):
        X.append(wifi_devices_values[i:i + seq_length])

    predictions = ml_model_wifi.predict(X)

    return jsonify(predictions.tolist()[:30])

