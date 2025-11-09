from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from flask_jwt_extended import create_access_token
from datetime import timedelta
import re

class UserController:
    @staticmethod
    def register_user():
        try:
            data = request.get_json()
            
            if not data:
                return make_response(jsonify({"erro": "Dados JSON são obrigatórios"}), 400)
            
            dados_obrigatorios = ["name", "email", "password", "cnpj", "phone"]
            info_faltantes = [item for item in dados_obrigatorios if item not in data]
            
            if info_faltantes:
                return make_response(
                    jsonify({"erro": f"Estão faltando os seguintes campos: {info_faltantes}"}), 
                    400
                )
            
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data["email"]):
                return make_response(jsonify({"erro": "E-mail inválido"}), 400)
            
            phone_str = str(data["phone"])
            phone_clean = re.sub(r'\D', '', phone_str)
            
            if len(phone_clean) not in [10, 11]:
                return make_response(
                    jsonify({"erro": "Telefone inválido. Use 10 ou 11 dígitos"}), 
                    400
                )
            
            if len(phone_clean) == 11 and not phone_clean[2] == '9':
                return make_response(jsonify({"erro": "Celular deve começar com 9"}), 400)
            
            data["phone"] = phone_clean
            
            result, status_code = UserService.create_user(**data)
            
            if status_code != 201:
                return make_response(jsonify(result), status_code)
            
            return make_response(jsonify({
                "mensagem": "Usuário criado com sucesso",
                "usuario": result.to_dict()
            }), 201)
            
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro interno do servidor {e}"}), 500)
    
    @staticmethod
    def login_user():
        try:
            data = request.get_json()
            
            if not data:
                return make_response(jsonify({"erro": "Dados JSON são obrigatórios"}), 400)
            
            result, status_code = UserService.login_user(**data)
            
            if status_code != 200:
                return make_response(jsonify(result), status_code)
            
            token = create_access_token(identity=str(result.id), expires_delta=timedelta(hours=1))

            return make_response(jsonify({
                "access_token": token,
                "token_type": "bearer",
                "expires_in": 3600,
                "user_id": result.id
            }), 200)
            
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    def activate_user(user_id):
        try:
            data = request.get_json()
            
            if not data:
                return make_response(jsonify({"erro": "Dados JSON são obrigatórios"}), 400)
            
            data["user_id"] = user_id
            result, status_code = UserService.activating_user(**data)
            return make_response(jsonify(result), status_code)
            
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    def get_user(user_id):
        """Busca usuário por ID"""
        try:
            result, status_code = UserService.get_user_by_id(user_id)
            return make_response(jsonify(result), status_code)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)
    
    @staticmethod
    def update_user(user_id):
        try:
            data = request.get_json()
            
            if not data:
                return make_response(jsonify({"erro": "Dados JSON são obrigatórios"}), 400)
            
            result, status_code = UserService.update_user(user_id, **data)
            return make_response(jsonify(result), status_code)
            
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)
    
    @staticmethod
    def delete_user(user_id):
        try:
            result, status_code = UserService.delete_user(user_id)
            return make_response(jsonify(result), status_code)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)