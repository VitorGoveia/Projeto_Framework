from src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    @app.route('/user', methods=['POST'])
    def route_register_user():
        return UserController.register_user()
    
    @app.route('/user', methods=['GET'])
    def route_get_users():
        return UserController.get_users()