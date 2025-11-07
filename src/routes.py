from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.product_controller import ProductController

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
    @jwt_required()
    def route_get_users(user_id):
        return UserController.get_user(user_id)

    @app.route('/user/<int:user_id>', methods=['PUT'])
    @jwt_required()
    def route_update_user(user_id):
        return UserController.update_user(user_id)

    @app.route('/user/<int:user_id>', methods=['DELETE'])
    @jwt_required()
    def route_delete_user(user_id):
        return UserController.delete_user(user_id)

    @app.route('/product/<int:product_id>', methods=['GET'])
    @jwt_required()
    def route_get_product(product_id):
        return ProductController.get_product(product_id)
    
    @app.route('/product/seller/<int:id_seller>', methods=['GET'])
    @jwt_required()
    def get_product_by_seller(id_seller):
        return ProductController.get_product_seller(id_seller)
 
    @app.route('/product', methods=['POST'])
    @jwt_required()
    def route_create_product():
        return ProductController.register_product()
    
    @app.route('/product/<int:product_id>', methods=['PUT'])
    @jwt_required()
    def route_update_product(product_id):
        return ProductController.update_product(product_id)
       
    @app.route('/product/<int:product_id>', methods=['DELETE'])
    @jwt_required()
    def route_delete_product(product_id):
        return ProductController.delete_product(product_id)
    

    
    @app.route('/sell/<int:sell_id>', methods=['GET'])
    @jwt_required()
    def route_get_sell(sell_id):
        return SellController.get_sell(sell_id)
    
    @app.route('/sell', methods=['POST'])
    @jwt_required()
    def route_create_sell():
        return SellController.register_sell()
    
    @app.route('/sell/<int:sell_id>', methods=['PUT'])
    @jwt_required()
    def route_update_sell(sell_id):
        return SellController.update_sell(sell_id)
       
    @app.route('/sell/<int:sell_id>', methods=['DELETE'])
    @jwt_required()
    def route_delete_sell(sell_id):
        return SellController.delete_product(sell_id)