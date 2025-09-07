from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from src.Infrastructure.Model.User_model import UserModel

class UserController:
    @staticmethod
    def register_user():
        """Cadastra o Usúario no DB"""
        data = request.get_json()

        dados_obrigatorios = ["name", "email", "password", "cnpj", "celular"]
        info_faltantes = []
        for item in data:
            if item not in dados_obrigatorios:
                info_faltantes.append(item)
        
        if info_faltantes:
            return make_response(jsonify({"erro": f"Estão faltando os seguintes campos: {info_faltantes}"}), 400)
        
        if not '@' in data["email"] or not '.com' in data["email"]:
            return make_response(jsonify({"erro": "E-mail inválido"}))
        
        try:
            if int(data["celular"]) < 13:
                return make_response(jsonify({"erro": "Numero de celular invalido. Formato: 5511912345678"}))
            
        except:
            return make_response(jsonify({"erro": "Celular invalido. Por favor, insira somente caracteres numericos"}))

        user = UserService.create_user(data["name"], data["email"], data["password"], data["celular"], data["cnpj"])
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)
    
    def get_users():
        "Busca todos os usuarios no DB"
        users = UserModel.query.all()
        return [{
            "Id": user.id,
            "Nome": user.name,
            "CNPJ": user.cnpj, 
            "E-mail": user.email,
            "Celular": user.phone,
            "Status": user.status
        }
        for user in users
        ]
    
    def update_user(user_id):
        data = request.get_json()
        print(data)
        update_user = UserService.update_user(user_id, data)

        if not update_user:
            return make_response(jsonify({"erro":"Usuário não encontrado!!!"}), 404)

        return jsonify ({
        "mensagem": "Usuário atualizado com sucesso!!!",
        "usuario": update_user.to_dict()
        })   
    
    def delete_user(user_id):
        sucess = UserService.delete_user(user_id)

        if not sucess:
            return make_response(jsonify({"erro":"Usuário não encontrado"}), 404)
        return jsonify({"mensagem": "Usuário deletado com sucesso!!!"})