from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.wifi_data_controller import api as wifi_ns
from .main.controller.cinema_data_controller import api as cinema_ns
from .main.controller.predict_controller import api as predict_ns
from .main.controller.aimodel_controller import api as aimodel_ns

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='CUPOLA-XS',
    version='1.0',
    description='',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(wifi_ns, path='/wifi')
api.add_namespace(cinema_ns, path='/cinema')
api.add_namespace(predict_ns, path='/predict')
api.add_namespace(aimodel_ns, path='/ai_model')  
