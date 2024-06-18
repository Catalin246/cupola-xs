from app.main import ml_model_wifi, ml_model_cinema

from app.main.service.wifi_data_service import get_all_wifi_data
from app.main.service.cinema_data_service import get_all_cinema_data

from datetime import timedelta


# using number 7 as the default sequence length because a week is 7 days long
def prepare_sequences(values, seq_length=7):
    sequences = []
    for i in range(len(values) - seq_length):
        sequences.append(values[i:i + seq_length])
    return sequences


def make_predictions(model, values, latest_date, predict_window=60, seq_length=7):
    sequences = prepare_sequences(values, seq_length)
    predictions = model.predict(sequences).tolist()

    responses = []
    for i in range(predict_window):
        next_day = latest_date + timedelta(days=i + 1)
        response = {
            'date': next_day.strftime('%d-%m-%Y'),
            'value': round(predictions[i][0])
        }
        responses.append(response)

    return responses


def predict_wifi_data():
    wifi_data = get_all_wifi_data()

    wifi_devices_values = [data.total_online_devices for data in wifi_data]
    latest_wifi_record_date = wifi_data[-1].date
    responses = make_predictions(ml_model_wifi, wifi_devices_values, latest_wifi_record_date)

    # Adjust the response keys for Wi-Fi data
    for response in responses:
        response['total_online_devices'] = response.pop('value')

    return responses


def predict_cinema_data():
    cinema_data = get_all_cinema_data()

    cinema_visitors_values = [data.visitors for data in cinema_data]
    latest_cinema_record_date = cinema_data[-1].date
    responses = make_predictions(ml_model_cinema, cinema_visitors_values, latest_cinema_record_date)

    # Adjust the response keys for cinema data
    for response in responses:
        response['visitors'] = response.pop('value')

    return responses

