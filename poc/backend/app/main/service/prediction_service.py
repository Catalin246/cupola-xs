from app.main import ml_model_cinema, ml_model_wifi_hourly

from app.main.service.wifi_data_service import get_all_wifi_data
from app.main.service.cinema_data_service import get_all_cinema_data
from ..model.aimodel import AIModel

from datetime import timedelta


# using number 7 as the default sequence length because a week is 7 days long
def prepare_sequences(values, seq_length):
    sequences = []
    for i in range(len(values) - seq_length):
        sequences.append(values[i:i + seq_length])
    return sequences

def make_cinema_predictions(model, values, latest_date, predict_window, seq_length=7):
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

def make_wifi_predictions(model, values, latest_date, predict_window, seq_length):
    sequences = prepare_sequences(values, seq_length)
    predictions = model.predict(sequences).tolist()

    responses = []

    for i in range(predict_window):
        hour = []
        hourly_values = []
        next_day = latest_date + timedelta(days=i + 1)

        max_value = max(predictions[i:i + 24])
        response = {
            'date': next_day.strftime('%d-%m-%Y'),
            'max_online_devices': round(max_value[0]),
            'hourly_values': []
        }
        for j in range(24):
            hour.append(latest_date + timedelta(hours=j + 1))
            hourly_values.append(predictions[i + j][0])

            hourly_data = {
                'hour': hour[j].strftime('%H:%M:%S'),
                'value': round(hourly_values[j])
            }

            response['hourly_values'].append(hourly_data)
        responses.append(response)
    return responses

def predict_wifi_data(predict_window):
    wifi_data = get_all_wifi_data()

    wifi_devices_values = [data.total_online_devices for data in wifi_data]
    latest_wifi_record_date = wifi_data[-1].date
    responses = make_wifi_predictions(ml_model_wifi_hourly, wifi_devices_values, latest_wifi_record_date, predict_window, 7)

    return responses


def predict_cinema_data(predict_window):
    cinema_data = get_all_cinema_data()

    cinema_visitors_values = [data.visitors for data in cinema_data]
    latest_cinema_record_date = cinema_data[-1].date
    responses = make_cinema_predictions(ml_model_cinema, cinema_visitors_values, latest_cinema_record_date, predict_window)

    # Adjust the response keys for cinema data
    for response in responses:
        response['visitors'] = response.pop('value')

    return responses


def get_metrics(model_type):
    all_models = AIModel.query.all()
    active_model = 0

    for model in all_models:
        if model.model_type==model_type and model.is_active:
            active_model = model

    return {
        'mean_squared_error': active_model.mean_squared_error,
        'mean_absolute_error': active_model.mean_absolute_error,
        'r2_score': active_model.r2_score
    }
