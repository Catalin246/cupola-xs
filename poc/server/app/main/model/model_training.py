# pandas as pd
import pandas as pd

import numpy as np

import matplotlib.pyplot as plt
    
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
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

    # Calculate the baseline prediction using the average of actual values
    baseline_prediction = np.mean(actual_values)
    baseline_predictions = np.full_like(actual_values, baseline_prediction)

    # Evaluate the baseline model using Mean Squared Error (MSE)
    baseline_mse = mean_squared_error(actual_values, baseline_predictions)
    print(f"Baseline Mean Squared Error (MSE): {baseline_mse}")

    # Calculate Root Mean Squared Error (RMSE) for the baseline model
    baseline_rmse = np.sqrt(baseline_mse)
    print(f"Baseline Root Mean Squared Error (RMSE): {baseline_rmse}")

    # Minimum value
    min_value = np.min(actual_values)
    print(f"Minimum value: {min_value}")

    # Maximum value
    max_value = np.max(actual_values)
    print(f"Maximum value: {max_value}")

    # Range
    range_value = max_value - min_value
    print(f"Range: {range_value}")

    # Mean Absolute Percentage Error (MAPE) for the baseline model
    baseline_mape = np.mean(np.abs((actual_values - baseline_predictions) / actual_values)) * 100
    print(f"Baseline Mean Absolute Percentage Error (MAPE): {baseline_mape}%")

    # Calculate R-squared (coefficient of determination) for the baseline model
    baseline_r2 = r2_score(actual_values, predictions)
    print(f"Baseline R-squared (Coefficient of Determination): {baseline_r2}")

    # Assuming 'actual_values' and 'predictions' are your actual and predicted values
    # Evaluate the model using Mean Squared Error (MSE)
    mse = mean_squared_error(actual_values, predictions)
    print(f"Mean Squared Error (MSE): {mse}")

    # Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)
    print(f"Root Mean Squared Error (RMSE): {rmse}")

    # Calculate additional metrics for the 'Visitors' value
    actual_values = np.array(actual_values)
    predictions = np.array(predictions)

    # Minimum value
    min_value = np.min(actual_values)
    print(f"Minimum value: {min_value}")

    # Maximum value
    max_value = np.max(actual_values)
    print(f"Maximum value: {max_value}")

    # Range
    range_value = max_value - min_value
    print(f"Range: {range_value}")

    # Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((actual_values - predictions) / actual_values)) * 100
    print(f"Mean Absolute Percentage Error (MAPE): {mape}%")
    # Calculate R-squared (coefficient of determination)
    r2 = r2_score(actual_values, predictions)
    print(f"R-squared (Coefficient of Determination): {r2}")

def train_wifi_model():
    wifi_data = pd.read_csv("data/wifi_data.csv", low_memory=False)
    wifi_data = wifi_data[['Date Time', 'Total Online Devices']]
    wifi_data = wifi_data.dropna()
    
    #Convert the value of the total number of the devices to an integer
    wifi_data['Total Online Devices'] = wifi_data['Total Online Devices'].str.replace('#','').astype(int)

    #Group all the all data based on the date. Add the total, mean, max and min of the devices conneted on a specific date
    dt = wifi_data['Date Time'].str.split(' ').str[0]
    devices = wifi_data['Total Online Devices']

    new_data_wifi_df = pd.DataFrame({'datetime': dt, 'totaldevices': devices})

    new_data_wifi_df = new_data_wifi_df[new_data_wifi_df['datetime'] != 'Averages']

    new_data_wifi_df['datetime'] = pd.to_datetime(new_data_wifi_df['datetime'], format='%d-%m-%Y')

    grouped_data = new_data_wifi_df.groupby('datetime').agg({'totaldevices': ['mean', 'max', 'min']})
    grouped_data.columns = grouped_data.columns.map(''.join)

    total_devices_sum = new_data_wifi_df.groupby('datetime')['totaldevices'].sum()

    sorted_grouped_wifi_data = pd.merge(grouped_data, total_devices_sum, left_index=True, right_index=True)

    sorted_grouped_wifi_data.rename(columns={'totaldevices': 'totaldevicessum'}, inplace=True)

    sorted_grouped_wifi_data = sorted_grouped_wifi_data.sort_index()

    wifi = sorted_grouped_wifi_data.copy()

    # Feature scaling
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(wifi['totaldevicesmean'].values.reshape(-1, 1))

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
    model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(seq_length, 1)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # Train the model
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), verbose=0)

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
    plt.ylabel('Total Devices Mean')
    plt.legend()
    plt.show()

    # Assuming 'actual_values' and 'predictions' are your actual and predicted values
    # Evaluate the model using Mean Squared Error (MSE)
    mse = mean_squared_error(actual_values, predictions)
    print(f"Mean Squared Error (MSE): {mse}")

    # Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)
    print(f"Root Mean Squared Error (RMSE): {rmse}")

    # Calculate additional metrics for the 'Visitors' value
    actual_values = np.array(actual_values)
    predictions = np.array(predictions)

    # Minimum value
    min_value = np.min(actual_values)
    print(f"Minimum value: {min_value}")

    # Maximum value
    max_value = np.max(actual_values)
    print(f"Maximum value: {max_value}")

    # Range
    range_value = max_value - min_value
    print(f"Range: {range_value}")

    # Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((actual_values - predictions) / actual_values)) * 100
    print(f"Mean Absolute Percentage Error (MAPE): {mape}%")

    # Calculate R-squared (coefficient of determination)
    r2 = r2_score(actual_values, predictions)
    print(f"R-squared (Coefficient of Determination): {r2}")

    # Feature scaling
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(wifi['totaldevicesmin'].values.reshape(-1, 1))

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
    model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(seq_length, 1)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # Train the model
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), verbose=0)

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
    plt.ylabel('Total Devices Min')
    plt.legend()
    plt.show()

    # Feature scaling
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(wifi['totaldevicesmax'].values.reshape(-1, 1))

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
    model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(seq_length, 1)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # Train the model
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), verbose=0)

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
    plt.ylabel('Total Devices Max')
    plt.legend()
    plt.show()

    # Assuming 'actual_values' and 'predictions' are your actual and predicted values
    # Evaluate the model using Mean Squared Error (MSE)
    mse = mean_squared_error(actual_values, predictions)
    print(f"Mean Squared Error (MSE): {mse}")

    # Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)
    print(f"Root Mean Squared Error (RMSE): {rmse}")

    # Calculate additional metrics for the 'Visitors' value
    actual_values = np.array(actual_values)
    predictions = np.array(predictions)

    # Minimum value
    min_value = np.min(actual_values)
    print(f"Minimum value: {min_value}")

    # Maximum value
    max_value = np.max(actual_values)
    print(f"Maximum value: {max_value}")

    # Range
    range_value = max_value - min_value
    print(f"Range: {range_value}")

    # Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((actual_values - predictions) / actual_values)) * 100
    print(f"Mean Absolute Percentage Error (MAPE): {mape}%")

    # Calculate R-squared (coefficient of determination)
    r2 = r2_score(actual_values, predictions)
    print(f"R-squared (Coefficient of Determination): {r2}")

train_cinema_model()
train_wifi_model()