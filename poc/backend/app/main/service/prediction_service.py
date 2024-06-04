from app.main import ml_model_wifi, ml_model_cinema, scaler_cinema

from app.main.service.wifi_data_service import get_all_wifi_data

from datetime import timedelta

def predict_wifi_data() :
    
    wifi_data = get_all_wifi_data()

    wifi_devices_values = []

    for data in wifi_data:
        wifi_devices_values.append(data.total_online_devices)

    X = []

    seq_length = 7

    for i in range(len(wifi_devices_values) - seq_length):
        X.append(wifi_devices_values[i:i + seq_length])

    predictions = ml_model_wifi.predict(X).tolist()

    latest_wifi_record = wifi_data[-1]

    responses = []

    for i in range(0, 30):
        next_day = latest_wifi_record.date + timedelta(days=i + 1)
        response ={
                'date': next_day.strftime('%d-%m-%Y'),
                'total_online_devices': round(predictions[i][0])
            }
        responses.append(response)

    #return jsonify(predictions.tolist()[:30])
    return responses

