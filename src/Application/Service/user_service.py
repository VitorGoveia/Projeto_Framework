#Aqui seria para cirar o usuario e já colocar a informação dele no banco de dados

from src.Config.db import db
from src.Infrastructure.Model.User_model import UserModel
from src.Domain.User import UserDomain
from werkzeug.security import check_password_hash
from src.Infrastructure.Http.whats_app import send_whatsapp_code


class UserService:
    @staticmethod
    def create_user(name, email, password, phone, cnpj, code): 
        new_user = UserDomain(name, email, password, phone, cnpj, code)
        user = UserModel(name=new_user.name, email=new_user.email, password=new_user.password, phone =new_user.phone, cnpj=new_user.cnpj, code=new_user.code)   
        
        #send_code = send_whatsapp_code(user.code,user.phone)
        
        user.to_dict()
        db.session.add(user)
        db.session.commit()
        return user
    
    def login_user(email, password):
        user = UserModel.query.filter_by(email=email).first()
        
        if not (password == user.password and email == user.email):
            return {
                "mensagem": "erro, informações inválidas",
                }, 400

        if not user:
            return {"Erro": "Usuário não encontrado!"}, 404
        
        if user.status != "Ativo":
            return {"Erro": "Usuário inativo, faça a autenticação de usuário"}, 403
        
        return user, 200
    
    def get_user_by_id(user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return {"Erro": "Usuário não encontrado"}

        return {
            "Id": user.id,
            "name": user.name,
            "cnpj": user.cnpj, 
            "email": user.email,
            "phone": user.phone,
            "status": user.status,
            "code": user.code
        }

    @staticmethod
    def update_user(user_id, data):
        user = UserModel.query.get(user_id)
        if not user:
            return None
        
        user.name = data.get("name", user.name)
        user.cnpj = data.get("cnpj", user.cnpj)
        user.email = data.get("email", user.email)
        user.phone = data.get("celular", user.phone)
        user.password = data.get("password", user.password)
        user.status = data.get("status", user.status)
        
        db.session.commit()
        return user
    
    @staticmethod
    def activating_user(code, email, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return None
        
        if str(code) == str(user.code) and email == user.email:

            user.status = "Ativo"
        
            db.session.commit()

            return {
                "mensagem": "Usuário ativado com sucesso!!!",
                "usuario": {"email": user.email, "nome": user.name}
                }, 200
        
        return {
                "mensagem": "erro, informações inválidas",
            }
        
    @staticmethod
    def delete_user(user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return None
        
        user.status = "Inativo"
        
        db.session.commit()
        return user