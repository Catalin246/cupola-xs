import csv
from io import StringIO
from flask import  request
from flask_restx import Resource
from ..util.dto import CinemaDataDto
from ..service.cinema_data_service import get_all_cinema_data, add_cinema_data_from_csv, delete_all_cinema_data
from typing import Dict, Tuple
from app.main.util.decorator import admin_token_required

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

    @api.expect(api.parser().add_argument('file', type=str, location='files'))
    @api.response(201, 'Data successfully added.')
    @api.doc('Add new cinema data from CSV.')
    @admin_token_required
    def post(self):
        """Add new cinema data from CSV"""
        csv_file = request.files['file']
        if not csv_file:
            return {'message': 'No file uploaded'}, 400
        
        # Read CSV file
        csv_data = csv_file.read().decode('utf-8')
        csv_stream = StringIO(csv_data)
        return add_cinema_data_from_csv(csv_stream)

    @api.doc('Delete all cinema data.')
    @api.response(204, 'Data successfully deleted.')
    def delete(self):
        """Delete all cinema data"""
        return delete_all_cinema_data()