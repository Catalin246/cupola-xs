from datetime import datetime
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
import numpy as np
from .. import db
from ..model.aimodel import AIModel
import os
from flask import abort

import os
from dotenv import load_dotenv, set_key

load_dotenv()

def get_all_models():
    return AIModel.query.all()

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def retrain_and_save_model(all_data, model_type):
    # Determine attribute to use based on model type
    if model_type == 'wifi':
        data_attribute = 'total_online_devices'
    elif model_type == 'cinema':
        data_attribute = 'visitors'
    else:
        raise ValueError("Invalid model type")

    # Convert to numpy array
    scaled_data = np.array([getattr(data, data_attribute) for data in all_data]).reshape(-1, 1)

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
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=0)

    # Calculate metrics
    mse = history.history['loss'][-1]
    mae = history.history['val_loss'][-1]
    r2 = 1 - (np.sum((y_test - model.predict(X_test))**2) / np.sum((y_test - np.mean(y_test))**2))

    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save the model with the date and time appended to the filename
    model_filename = f"models/{model_type}/{model_type}data_model_{current_datetime}.h5"
    model.save(model_filename)

    # Save the model details in the database
    new_model = AIModel(
        model_name=model_filename,
        mean_squared_error=mse,
        mean_absolute_error=mae,
        r2_score=r2,
        model_type=model_type,
        is_active=False
    )
    db.session.add(new_model)
    db.session.commit()

def delete_model(model_id):
    # Query the model from the database by ID
    model = AIModel.query.get(model_id)
    
    if model is None:
        abort(404, description="Model not found")
    
    # Check if the model is active
    if model.is_active:
        raise ValueError("The model is currently in use and cannot be deleted.")
    
    # Delete the model file from the filesystem
    try:
        if os.path.exists(model.model_name):
            os.remove(model.model_name)
        else:
            raise FileNotFoundError(f"The model file {model.model_name} does not exist.")
    except Exception as e:
        raise e
    
    # Remove the model entry from the database
    db.session.delete(model)
    db.session.commit()

def update_model_is_active(model_id):
    # Query the model from the database by ID
    model = AIModel.query.get(model_id)
    
    if model is None:
        abort(404, description="Model not found")
    
    # Ensure only one model of each type is active
    if model.is_active:
        raise ValueError("This model is already active.")
    
    # Get all models of the same type
    all_models_of_same_type = AIModel.query.filter_by(model_type=model.model_type).all()

    # Deactivate all models of the same type
    for other_model in all_models_of_same_type:
        if other_model.is_active:
            other_model.is_active = False
            db.session.add(other_model)
    
    # Activate the selected model
    model.is_active = True
    db.session.add(model)
    db.session.commit()

    # Update the .env file with the new active model path
    env_file = '.env'
    key = f'{model.model_type.upper()}_MODEL_PATH'
    value = model.model_name
    set_key(env_file, key, value)

    # Reload .env variables
    load_dotenv()