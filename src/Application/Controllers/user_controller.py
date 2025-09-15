from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from src.Infrastructure.Model.User_model import UserModel
from flask_jwt_extended import create_access_token
from datetime import timedelta
import random

class UserController:
    @staticmethod
    def register_user():
        """Cadastra o Usúario no DB"""
        data = request.get_json()

        dados_obrigatorios = ["name", "email", "password", "cnpj", "phone"]
        info_faltantes = []
        for item in dados_obrigatorios:
            if item not in data:
                info_faltantes.append(item)
        
        if info_faltantes:
            return make_response(jsonify({"erro": f"Estão faltando os seguintes campos: {info_faltantes}"}), 400)
        
        if not '@' in data["email"] or not '.com' in data["email"]:
            return make_response(jsonify({"erro": "E-mail inválido"}))
        
        try:
            if len((data["phone"])) < 13:
                return make_response(jsonify({"erro": "Numero de celular invalido. Formato: 5511912345678"}))
            
        except:
            return make_response(jsonify({"erro": "Celular invalido. Por favor, insira somente caracteres numericos"}))

        #Código para validação na Twilio
        new_code = random.randint(1000, 9999)

        user = UserService.create_user(data["name"], data["email"], data["password"], data["phone"], data["cnpj"], new_code)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)
    
    def activate_user(user_id):
        """Ativa o usuario"""
        data = request.get_json()
        email = data.get("email")
        code = data.get("code")

        user = UserModel.query.get(user_id)
        if str(code) == str(user.code) and email == user.email:
            activate_user = UserService.activating_user(user_id)

            return make_response(jsonify ({
                "mensagem": "Usuário ativado com sucesso!!!",
                "usuario": {"email": activate_user.email, "nome": activate_user.name}
                }))
        return make_response(jsonify ({
                "mensagem": "erro, informações inválidas",
                }))
            
    def login_user():
        """Faz o login, retorna o TOKEN"""
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return make_response(jsonify({"erro":"Email e senha são obrigatórios"}), 400)
        
        user_find = UserModel.query.filter_by(email=email).first()
        if not (password == user_find.password and email == user_find.email):
            return make_response(jsonify ({
                "mensagem": "erro, informações inválidas",
                }))
        
        user, status = UserService().login_user(email, password)
        if status != 200:
            return make_response(jsonify(user), status)
        
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
    
        return make_response(jsonify({"access_token": token}), 200)

    def get_user(user_id):
        "Busca o usuario no DB"
        user = UserModel.query.get(user_id)
        return {
            "Id": user.id,
            "name": user.name,
            "cnpj": user.cnpj, 
            "email": user.email,
            "phone": user.phone,
            "status": user.status,
            "code": user.code
        }
    
    def update_user(user_id):
        """Atualiza os dados do Usuario"""
        data = request.get_json()
        update_user = UserService.update_user(user_id, data)

        if not update_user:
            return make_response(jsonify({"erro":"Usuário não encontrado!!!"}), 404)

        return jsonify ({
        "mensagem": "Usuário atualizado com sucesso!!!",
        "usuario": update_user.to_dict()
        })   
    
    def delete_user(user_id):
        """Inativa o Usuario"""
        sucess = UserService.delete_user(user_id)

        if not sucess:
            return make_response(jsonify({"erro":"Usuário não encontrado"}), 404)
        return jsonify({"mensagem": "Usuário deletado com sucesso!!!"})