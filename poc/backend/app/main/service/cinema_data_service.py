import csv
from io import StringIO
from app.main import db
from app.main.model.cinemadata import CinemaData
from datetime import date
from datetime import datetime
from typing import Dict, Tuple, Union

from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
from dateutil import parser as date_parser

def get_all_cinema_data():
    return CinemaData.query.all()

def add_cinema_data_from_csv(csv_stream: StringIO) -> Tuple[Dict[str, str], int]:
    try:
        reader = csv.DictReader(csv_stream, delimiter=';')
        for row in reader:
            if not row['Visitor']:
                continue

            if not row['Date']:
                continue

            if not row['Day']:
                continue

            try:
                parsed_date = date_parser.parse(row['Date']).date()
            except (ValueError, TypeError):
                continue

            existing_record = CinemaData.query.filter_by(date=parsed_date).first()
            if existing_record:
                existing_record.day = row['Day']
                existing_record.visitors = int(row['Visitor'])
                save_changes(existing_record)
            else:
                new_cinema_data = CinemaData(
                day=row['Day'],
                date=parsed_date,
                visitors=int(row['Visitor'])
            )
                save_changes(new_cinema_data)
            

        response_object = {
            'status': 'success',
            'message': 'Successfully added data from CSV.',
        }
        retrain_and_save_cinema_model()

        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.',
            'error': str(e)
        }
        return response_object, 400

def save_changes(data: Union[CinemaData, None]) -> None:
    if data:
        db.session.add(data)
        db.session.commit()

def delete_all_cinema_data():
    try:
        # Delete all records from the table
        CinemaData.query.delete()
        db.session.commit()
        return None, 204
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred while deleting data. Please try again.',
            'error': str(e)
        }
        return response_object, 500

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def retrain_and_save_cinema_model():
    # Retrieve all cinema data
    all_data = get_all_cinema_data()

    # Convert to numpy array
    scaled_data = np.array([data.visitors for data in all_data]).reshape(-1, 1)

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

    # Save the model
    model.save("cinemadata_model.h5")

