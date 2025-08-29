'''from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
#from src.Infrastructure.Model.User_model import User

#USER SERVICE AINDA NÃO ESTÁ FUNCIONANDO

class UserController:
    @staticmethod
    def register_user():
        """Cadastra o Usúario no DB"""
        data = request.get_json()

        dados_obrigatorios = ["name", "email", "password", "cnpj", "celular"]
        info_faltantes = []
        for item in data:
            if item not in dados_obrigatorios:
                info_faltantes.append[item]
        
        if info_faltantes:
            return make_response(jsonify({"erro": f"Estão faltando os seguintes campos: {info_faltantes}"}), 400)

        user = UserService.create_user(data.name, data.email, data.password, data.celular, data.cnpj)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)
    
    def get_users():
        "Busca todos os usuarios no DB"
        users = User.query.all()
        return [{
            "Id": user.id,
            "Nome": user.name,
            "CNPJ": user.cnpj, 
            "E-mail": user.email,
            "Celular": user.celular,
            "Status": user.status
        }
        for user in users
        ]
'''