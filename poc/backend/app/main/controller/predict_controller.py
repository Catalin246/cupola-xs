from flask import request

from flask_restx import Resource

from ..service.prediction_service import predict_wifi_data, predict_cinema_data, get_metrics

from app.main.util.dto import WifiPredictDto
from app.main.util.dto import CinemaPredictDto

api = WifiPredictDto.api
api = CinemaPredictDto.api
prediction_wifi = WifiPredictDto.prediction_wifi
prediction_cinema = CinemaPredictDto.prediction_cinema

@api.route("/wifi")
class WifiPrediction(Resource):
    @api.doc('predict total online devices based on date')
    def post(self):
        return predict_wifi_data(60)
    
@api.route("/cinema")
class CinemaPrediction(Resource):
    @api.doc('predict total cinema visitors based on date')
    def post(self):
        return predict_cinema_data(60)

@api.route("/cinema/metrics")
class CinemaMetrics(Resource):
    @api.doc('get metrics for cinema model')
    def get(self):
        return get_metrics('cinema')

@api.route("/wifi/metrics")
class WifiMetrics(Resource):
    @api.doc('get metrics for wifi model')
    def get(self):
        return get_metrics('wifi')