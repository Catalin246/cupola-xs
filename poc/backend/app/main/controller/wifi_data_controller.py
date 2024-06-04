import csv
from io import StringIO
from flask import request, jsonify
from flask_restx import Resource
from ..service.wifi_data_service import get_all_wifi_data, add_wifi_data, add_wifi_data_from_csv, delete_wifi_data
from app.main.util.dto import WifiDataDto
from app.main.util.decorator import admin_token_required

api = WifiDataDto.api
_wifiData = WifiDataDto.wifi_data

@api.route('/')
class WifiList(Resource):
    @api.doc('List of wifi data')
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

   
    @api.expect(api.parser().add_argument('file', type=str, location='files'))
    @api.response(201, 'Data successfully added.')
    @api.doc('Add new wifi data from CSV.')
    @admin_token_required
    def post(self):
        """Add new wifi data from CSV"""
        csv_file = request.files['file']
        if not csv_file:
            return {'message': 'No file uploaded'}, 400
        
        # Read CSV file
        csv_data = csv_file.read().decode('utf-8')
        csv_stream = StringIO(csv_data)
        return add_wifi_data_from_csv(csv_stream)
    
    
    @api.doc('Delete all wifi data.')
    @api.response(204, 'Data successfully deleted.')
    def delete(self):
        """Delete all wifi data"""
        return delete_wifi_data()