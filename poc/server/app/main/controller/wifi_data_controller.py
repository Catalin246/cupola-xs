from flask import request, jsonify
from flask_restx import Resource
from ..service.wifi_data_service import get_all_wifi_data, add_wifi_data
from app.main.util.dto import WifiDataDto

api = WifiDataDto.api
_wifiData = WifiDataDto.wifi_data

@api.route('/')
class WifiList(Resource):
    @api.doc('List of registered users')
    #@admin_token_required
    @api.marshal_list_with(_wifiData, envelope='data')
    def get(self):
        return get_all_wifi_data()
    
    #@admin_token_required
    @api.expect(_wifiData, validate=True)
    @api.response(201, 'Wifi Data Successfully Uploaded')
    @api.doc('Upload Wifi Data')
    def post(self):
        data = request.json
        return add_wifi_data(data)
