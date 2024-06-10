import csv
from io import StringIO
from flask import request, jsonify
from flask_restx import Resource
from ..service.wifi_data_service import get_all_wifi_data, add_wifi_data, add_wifi_data_from_csv, delete_wifi_data
from app.main.util.dto import WifiDataDto
from app.main.util.decorator import admin_token_required
from werkzeug.datastructures import FileStorage

api = WifiDataDto.api
_wifiData = WifiDataDto.wifi_data

@api.route('/')
class WifiList(Resource):
    @api.doc('List of wifi data')
    #@admin_token_required
    @api.marshal_list_with(_wifiData, envelope='data')
    def get(self):
        return get_all_wifi_data()

   
    @api.expect(api.parser().add_argument('file', type=FileStorage, location='files'))
    @api.response(201, 'Data successfully added.')
    @api.doc('Add new wifi data from CSV.')
    @admin_token_required
    def post(self):
        """Add new wifi data from CSV"""
        file = request.files['file']
        if not file:
            return {'message': 'No file uploaded'}, 400
        
        if not file.filename.endswith('.csv'):
            return {'message': 'Uploaded file is not a CSV'}, 400
        
        # Read CSV file
        csv_data = file.read().decode('utf-8')
        csv_stream = StringIO(csv_data)

        # Check if the CSV file has the required columns
        reader = csv.DictReader(csv_stream)
        required_columns = {'Total Online Devices', 'Date Time'}
        if not required_columns.issubset(reader.fieldnames):
            return {'message': 'CSV file does not contain the required columns, please upload the correct file'}, 400

        # Reset the StringIO object to the beginning
        csv_stream.seek(0)

        return add_wifi_data_from_csv(csv_stream)
    
    
    @api.doc('Delete all wifi data.')
    @api.response(204, 'Data successfully deleted.')
    def delete(self):
        """Delete all wifi data"""
        return delete_wifi_data()