from flask import request, jsonify
from flask_restx import Resource
from ..service.wifi_data_service import get_all_wifi_data
from app.main.util.dto import WifiDataDto

api = WifiDataDto.api
_wifiData = WifiDataDto.wifi_data

# @api.route('/', methods=['POST'])
# def create_wifi_data():
#     data = request.get_json()
#     wifi_data_dto = WifiDataDto(**data)
#     wifi_data = WifiDataService.add_wifi_data(wifi_data_dto)
#     return jsonify({'id': wifi_data.id, 'date': wifi_data.datetime, 'total_online_devices': wifi_data.total_online_devices}), 201

@api.route('/', methods=['GET'])
class WifiList(Resource):
    @api.marshal_list_with(_wifiData, envelope='data')
    def get(self):
        return get_all_wifi_data()
    
# @api.route('/<int:wifi_data_id>', methods=['GET'])
# def get_wifi_data_by_id(wifi_data_date):
#     wifi_data = WifiDataService.get_wifi_data_by_date(wifi_data_date)
#     if wifi_data:
#         return jsonify({'id': wifi_data.id, 'date': wifi_data.datetime, 'total_online_devices': wifi_data.total_online_devices})
#     else:
#         return jsonify({'message': 'WiFi data not found'}), 404

# @api.route('/<int:wifi_data_id>', methods=['DELETE'])
# def delete_wifi_data(wifi_data_date):
#     wifi_data = WifiDataService.delete_wifi_data(wifi_data_date)
#     if wifi_data:
#         return jsonify({'message': 'WiFi data deleted'})
#     else:
#         return jsonify({'message': 'WiFi data not found'}), 404
