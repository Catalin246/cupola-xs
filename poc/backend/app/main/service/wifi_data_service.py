import csv
from io import StringIO
from datetime import datetime
from app.main import db
from ..model.wifi_data import WifiData
from typing import Dict, Tuple, Union
import re
from flask import jsonify

from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np

def get_all_wifi_data():
    return WifiData.query.all()

def get_wifi_data_by_date(wifi_data_date):
    return WifiData.query.get(wifi_data_date)

def get_earliest_wifi_data():
    return WifiData.query.order_by(WifiData.date).first()

def add_wifi_data(data: Dict[str, str]) -> None:
    new_wifi_data = WifiData(
        date = datetime.strptime(data['date'], '%d-%m-%Y'),
        total_online_devices = data['total_online_devices']
    )

def add_wifi_data_from_csv(csv_stream: StringIO) -> Tuple[Dict[str, str], int]:
    try:
        reader = csv.DictReader(csv_stream, delimiter=',')
        for row in reader:
            if not row['Total Online Devices']:
                continue

            if not row['Date Time']:
                continue

            cleaned_value = re.sub(r'\D', '', row['Total Online Devices'])
            if cleaned_value.isdigit():
                total_online_devices = int(cleaned_value)
                date_time_str = row["Date Time"].split(' - ')[0]
                try:
                    date_time_obj = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M:%S')
                except ValueError:
                    continue

                existing_record = WifiData.query.filter_by(date=date_time_obj).first()
                if existing_record:
                    existing_record.total_online_devices = total_online_devices
                    add_to_database(existing_record)
                else:
                    new_wifi_data = WifiData(
                        date=date_time_obj,
                        total_online_devices=total_online_devices
                    )
                    add_to_database(new_wifi_data)
            else:
                continue

        retrain_and_save_wifi_model()

        return {
            'status': 'success',
            'message': 'Successfully added data from CSV.',
        }, 201

    except Exception as e:
        return {
            'message': str(e)
        }, 500


def delete_wifi_data():
  try:
        # Delete all records from the table
        WifiData.query.delete()
        db.session.commit()
        return None, 204
  except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred while deleting data. Please try again.',
            'error': str(e)
        }
        return response_object, 500

def add_to_database(data: WifiData) -> None:
    db.session.add(data)
    db.session.commit()

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def retrain_and_save_wifi_model():
    # Convert to numpy array
    all_data = get_all_wifi_data()

   # Convert to numpy array
    scaled_data = np.array([data.total_online_devices for data in all_data]).reshape(-1, 1)

    # Define sequence length
    seq_length = 7

    # Create sequences for LSTM input
    X, y = create_sequences(scaled_data, seq_length)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Reshape data to fit LSTM input requirements
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    # Define LSTM model architecture
    model = Sequential()
    model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(seq_length, 1)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

    # Train the model
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=0)

    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save the model with the date and time appended to the filename
    model_filename = f"models/wifi/wifidata_model_{current_datetime}.h5"
    model.save(model_filename)
