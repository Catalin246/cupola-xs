import csv
from io import StringIO
from flask import  request
from flask_restx import Resource
from ..util.dto import CinemaDataDto
from ..service.cinema_data_service import get_all_cinema_data, add_cinema_data_from_csv, delete_all_cinema_data
from typing import Dict, Tuple
from app.main.util.decorator import admin_token_required
from werkzeug.datastructures import FileStorage

api = CinemaDataDto.api
_cinemaData = CinemaDataDto.cinema_data

@api.route('/')
class CinemaList(Resource):
    @api.doc('List of visitors that come to the cinema ')
    @api.param('start_date', 'Start date in the format DD-MM-YYYY')
    @api.param('end_date', 'End date in the format DD-MM-YYYY')
    @api.marshal_list_with(_cinemaData, envelope='data')
    def get(self):
        """List all visitors of cinema """
        return get_all_cinema_data()

    @api.expect(api.parser().add_argument('file', type=FileStorage, location='files'))
    @api.response(201, 'Data successfully added.')
    @api.doc('Add new cinema data from CSV.')
    @admin_token_required
    def post(self):
        """Add new cinema data from CSV"""
        file = request.files['file']
        if not file:
            return {'message': 'No file uploaded'}, 400
    
        if not file.filename.endswith('.csv'):
            return {'message': 'Uploaded file is not a CSV'}, 400

        # Read CSV file
        csv_data = file.read().decode('utf-8')
        csv_stream = StringIO(csv_data)

         # Check if the CSV file has the required columns
        reader = csv.DictReader(csv_stream, delimiter=';')
        required_columns = {'Day','Date','Visitor'}
        
        if not required_columns.issubset(reader.fieldnames):
            return {'message': 'CSV file does not contain the required columns, please upload the correct file'}, 400

        # Reset the StringIO object to the beginning
        csv_stream.seek(0)

        return add_cinema_data_from_csv(csv_stream)

    @api.doc('Delete all cinema data.')
    @api.response(204, 'Data successfully deleted.')
    def delete(self):
        """Delete all cinema data"""
        return delete_all_cinema_data()