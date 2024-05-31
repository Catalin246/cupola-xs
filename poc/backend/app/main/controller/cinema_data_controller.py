from flask import  request
from flask_restx import Resource

from ..util.dto import CinemaDataDto
from ..service.cinema_data_service import get_all_cinema_data, add_cinema_data
from typing import Dict, Tuple

api = CinemaDataDto.api
_cinemaData = CinemaDataDto.cinema_data


@api.route('/')
class CinemaList(Resource):
    @api.doc('List of visitors that come to the cinema within a specific date range')
    @api.param('start_date', 'Start date in the format DD-MM-YYYY')
    @api.param('end_date', 'End date in the format DD-MM-YYYY')
    @api.marshal_list_with(_cinemaData, envelope='data')
    def get(self):
        """List all visitors of cinema within a specific date range"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        return get_all_cinema_data(start_date, end_date)

    @api.expect(_cinemaData, validate = True)
    @api.response(201, 'Data successfully added.')
    @api.doc('Add new cinema data.')
    def post(self)-> Tuple[Dict[str, str], int]:
        """Add new cinema data """
        data = request.json
        return add_cinema_data(data = data)