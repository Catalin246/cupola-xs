from app.main import ml_model_wifi, scaler_wifi, ml_model_cinema, scaler_cinema

from app.main.service.wifi_data_service import get_earliest_wifi_data

from flask import jsonify

from typing import Dict, Tuple
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

def predict_wifi_data(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    date = datetime.strptime(data['date'], '%d-%m-%Y')
    
    first_wifi_data = get_earliest_wifi_data()

    print(first_wifi_data.date)

    days_to_predict = []

    for i in range(0, 7):

        days_difference = (date - first_wifi_data.date).days

        print(days_difference)

        days_difference_array = np.array([[days_difference]])

        print(days_difference_array)

        days_to_predict.append(days_difference_array)

        date += timedelta(days=1)

    days_to_predict = np.concatenate(days_to_predict, axis=0)

    predictions = ml_model_wifi.predict(days_to_predict)

    predictions = scaler_wifi.inverse_transform(predictions)

    return jsonify(predictions.tolist())

