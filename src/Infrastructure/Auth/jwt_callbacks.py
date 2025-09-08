from flask import jsonify

def register_jwt_callbacks(jwt):
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"erro": "Token expirado"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({"erro": "Token inválido"}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return jsonify({"erro": "Token não encontrado"}), 401