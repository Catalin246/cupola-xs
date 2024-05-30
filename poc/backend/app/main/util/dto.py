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