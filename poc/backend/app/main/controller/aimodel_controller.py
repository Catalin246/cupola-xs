import csv
from io import StringIO
from flask import request, abort
from flask_restx import Resource
from ..service.wifi_data_service import get_all_wifi_data
from ..service.cinema_data_service import get_all_cinema_data
from ..service.aimodel_service import retrain_and_save_model, get_all_models, delete_model, update_model_is_active
from app.main.util.dto import AIModelDto
from app.main.util.decorator import admin_token_required
from werkzeug.datastructures import FileStorage

api = AIModelDto.api
_aimodel = AIModelDto.ai_model

@api.route('/')
class AIModelList(Resource):
    @api.marshal_list_with(_aimodel, envelope='models')
    @admin_token_required
    @api.doc('Get all models')
    def get(self):
        """Get all models"""
        return get_all_models()

@api.route('/retrain')
class AIModelRetrain(Resource):
    @api.expect(api.parser().add_argument('type', type=str, location='form', required=True, help='Type of model (wifi/cinema)'))
    @api.response(201, 'Model successfully retrained and saved.')
    @api.doc('Retrain and save model')
    @admin_token_required
    def post(self):
        """Retrain and save model"""
        model_type = request.form.get('type')
        if model_type not in ['wifi', 'cinema']:
            return {'message': 'Invalid model type'}, 400
        
        # Fetch all data based on the model type
        if model_type == 'wifi':
            all_data = get_all_wifi_data()
        elif model_type == 'cinema':
            all_data = get_all_cinema_data()

        # Retrain and save the model
        retrain_and_save_model(all_data, model_type)

        return {'message': f'{model_type.capitalize()} model retrained and saved successfully'}, 201

@api.route('/<int:model_id>')
@api.param('model_id', 'The Model identifier')
class AIModel(Resource):
    @api.response(204, 'Model successfully deleted.')
    @api.doc('Delete a model')
    @admin_token_required
    def delete(self, model_id):
        """Delete a model"""
        try:
            delete_model(model_id)
            return '', 204
        except ValueError as e:
            abort(400, description=str(e))
        except FileNotFoundError as e:
            abort(404, description=str(e))
        except Exception as e:
            abort(500, description=str(e))

    @api.response(200, 'Model successfully updated.')
    @api.doc('Update a model')
    @admin_token_required
    def put(self, model_id):
        """Update a model"""
        try:
            update_model_is_active(model_id)
            return {'message': 'Model successfully updated'}, 200
        except ValueError as e:
            abort(400, description=str(e))
        except Exception as e:
            abort(500, description=str(e))