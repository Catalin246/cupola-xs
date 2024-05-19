# pandas as pd
import pandas as pd

import numpy as np

import matplotlib.pyplot as plt
    
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import GridSearchCV

def train_cinema_model():
    cinema = pd.read_csv('data\cinema.csv', sep=';', low_memory=False)

    # Mapping dictionary for translating Dutch day names to English
    dutch_to_english = {
        'Zondag': 'Sunday',
        'maandag': 'Monday',
        'dinsdag': 'Tuesday',
        'woensdag': 'Wednesday',
        'donderdag': 'Thursday',
        'vrijdag': 'Friday',
        'zaterdag': 'Saturday'
    }

    # Translate Dutch day names to English
    cinema['Day'] = cinema['Day'].map(dutch_to_english)

    # Convert the "Date" column to datetime
    cinema['Date'] = pd.to_datetime(cinema['Date'], format='%d/%m/%Y')

    # Drop rows with missing values in the "Visitor" column
    cinema = cinema.dropna(subset=['Visitor'])

    # Convert the "Visitor" column to numeric to check for non-numeric values
    cinema['Visitor'] = pd.to_numeric(cinema['Visitor'], errors='coerce')

    # Drop rows with non-numeric values in the "Visitor" column
    cinema = cinema.dropna(subset=['Visitor'])

    # Convert the "Visitor" column to integer
    cinema['Visitor'] = cinema['Visitor'].astype(int)

    # Extract each column into separate variables
    day_categorical = cinema['Day'].astype('category')
    date = cinema['Date']
    visitor = cinema['Visitor']

    # Feature scaling
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(cinema['Visitor'].values.reshape(-1, 1))

    # Prepare data for LSTM
    def create_sequences(data, seq_length):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)

    # Define sequence length
    seq_length = 7

    # Create sequences for LSTM input
    X, y = create_sequences(scaled_data, seq_length)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Define LSTM model architecture
    model = Sequential()
    model.add(LSTM(50, activation='tanh', return_sequences=True, input_shape=(seq_length, 1)))
    model.add(LSTM(50, activation='tanh'))
    model.add(Dense(1))

    # Define optimizer with learning rate
    optimizer = Adam(learning_rate=0.001)

    model.compile(optimizer=optimizer, loss='mse')

    # Train the model with specified epochs
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=0)

    # Evaluate the model
    loss = model.evaluate(X_test, y_test, verbose=0)
    print(f"LSTM Model Test Loss: {loss}")

    # Make predictions
    predictions = model.predict(X_test)

    # Inverse scale the predictions
    predictions = scaler.inverse_transform(predictions)

    # Inverse scale the actual values for plotting
    actual_values = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Plot actual vs. predicted visitor numbers
    y_train_actual = scaler.inverse_transform(y_train.reshape(-1, 1))

    train_length = len(y_train_actual)

    plt.figure(figsize=(12, 6))
    plt.plot(range(train_length), y_train_actual, label='Actual (Training)')
    plt.plot(range(train_length, train_length+len(actual_values)), actual_values, label='Actual (Testing)')
    plt.plot(range(train_length, train_length+len(predictions)), predictions, label='Predicted (Testing)')
    plt.title('Actual vs. Predicted Visitors')
    plt.xlabel('Time')
    plt.ylabel('Number of Visitors')
    plt.legend()
    plt.show()

def tune_hyperparameters():
    return "Cool"

train_cinema_model()