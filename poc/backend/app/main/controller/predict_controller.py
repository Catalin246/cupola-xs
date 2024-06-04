from flask import request

from flask_restx import Resource

from ..service.prediction_service import predict_wifi_data

from app.main.util.dto import WifiPredictDto

api = WifiPredictDto.api
prediction_wifi = WifiPredictDto.prediction_wifi

@api.route("/wifi")
class WifiPrediction(Resource):
    @api.doc('predict total online devices based on date')
    def post(self):
        return predict_wifi_data()