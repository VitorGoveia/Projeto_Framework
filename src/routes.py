from flask import jsonify, make_response
from src.Application.Controllers.user_controller import UserController
from flask_jwt_extended import jwt_required

def register_routes(app):
    @app.route('/user', methods=['POST'])
    def route_register_user():
        return UserController.register_user()
    
    @app.route('/login', methods=['POST'])
    def route_login_user():
        return UserController.login_user()
    
    @app.route('/activate/<int:user_id>', methods=['POST'])
    def route_activate_user(user_id):
        return UserController.activate_user(user_id)

    @app.route('/user/<int:user_id>', methods=['GET'])
    #@jwt_required()
    def route_get_users(user_id):
        return UserController.get_user(user_id)

    @app.route('/user/<int:user_id>', methods=['PUT'])
    #@jwt_required()
    def route_update_user(user_id):
        return UserController.update_user(user_id)

    @app.route('/user/<int:user_id>', methods=['DELETE'])
    @jwt_required()
    def route_delete_user(user_id):
        return UserController.delete_user(user_id)