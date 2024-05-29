from flask import Blueprint, request, jsonify
from app.main.service.services import WifiDataService
from app.main.util.dto import WifiDataDto
from pydantic import ValidationError

wifi_data_bp = Blueprint('wifi_data_bp', __name__)

@wifi_data_bp.route('/', methods=['POST'])
def create_wifi_data():
    data = request.get_json()
    try:
        wifi_data_dto = WifiDataDto(**data)
        wifi_data = WifiDataService.add_wifi_data(wifi_data_dto)
        return jsonify({'id': wifi_data.id, 'date': wifi_data.datetime, 'total_online_devices': wifi_data.total_online_devices}), 201
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

@wifi_data_bp.route('/', methods=['GET'])
def get_all_wifi_data():
    wifi_data_list = WifiDataService.get_all_wifi_data()
    return jsonify([{'id': data.id, 'date': data.datetime, 'total_online_devices': data.total_online_devices} for data in wifi_data_list])

@wifi_data_bp.route('/<int:wifi_data_id>', methods=['GET'])
def get_wifi_data_by_id(wifi_data_date):
    wifi_data = WifiDataService.get_wifi_data_by_date(wifi_data_date)
    if wifi_data:
        return jsonify({'id': wifi_data.id, 'date': wifi_data.datetime, 'total_online_devices': wifi_data.total_online_devices})
    else:
        return jsonify({'message': 'WiFi data not found'}), 404

@wifi_data_bp.route('/<int:wifi_data_id>', methods=['DELETE'])
def delete_wifi_data(wifi_data_date):
    wifi_data = WifiDataService.delete_wifi_data(wifi_data_date)
    if wifi_data:
        return jsonify({'message': 'WiFi data deleted'})
    else:
        return jsonify({'message': 'WiFi data not found'}), 404
