from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class WifiDataDto:
    api = Namespace('wifi', description = 'wifi data related operations')
    wifi_data = api.model('wifi', {
        'date': fields.DateTime(required=True, description='date of device being online'),
        'total_online_devices': fields.String(required=True, description='total online devices of the day')
    })

class CinemaDataDto:
    api = Namespace('cinema', description= 'cinema data related operations')
    cinema_data = api.model('cinema', {
        'day' : fields.String(required = True, description = 'Day of the week for number of visitors'),
        'date' : fields.Date(required = True, description = 'Date of how many visitors came'),
        'visitors': fields.Integer(required = True, description = 'Number of visitors that came that day')
    })
class WifiPredictDto:
    api = Namespace('prediction_wifi', description="Wi-Fi Connected Devices Predictions made by the model")
    prediction_wifi = api.model('prediction_wifi', {
        'date': fields.DateTime(required=True, description='date of device being online')
    })

class CinemaPredictDto:
    api = Namespace('prediction_cinema', description="Cinema Visitors Predictions made by the model")
    prediction_cinema = api.model('prediction_cinema', {
        'date': fields.DateTime(required=True, description='date of visitors being at Cupola')
    })

class AIModelDto:
    api = Namespace('ai_model', description='AI model related operations')
    ai_model = api.model('ai_model', {
        'id': fields.Integer(required=True, description='ID of the model'),
        'date': fields.DateTime(required=True, description='Date when the model was created'),
        'model_name': fields.String(required=True, description='Name of the model'),
        'is_active': fields.Boolean(required=True, description='Is the model active'),
        'mean_squared_error': fields.Float(required=True, description='Mean Squared Error of the model'),
        'mean_absolute_error': fields.Float(required=True, description='Mean Absolute Error of the model'),
        'r2_score': fields.Float(required=True, description='R² Score of the model'),
        'model_type': fields.String(required=True, description='Type of the model (wifi/cinema)')
    })