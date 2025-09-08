#Aqui seria para cirar o usuario e já colocar a informação dele no banco de dados

from src.Config.db import db
from src.Infrastructure.Model.User_model import UserModel
from src.Domain.User import UserDomain
from werkzeug.security import check_password_hash


class UserService:
    @staticmethod
    def create_user(name, email, password, phone, cnpj):
        new_user = UserDomain(name, email, password, phone, cnpj)
        user = UserModel(name=new_user.name, email=new_user.email, password=new_user.password, phone =new_user.phone, cnpj=new_user.cnpj)  
        user.to_dict()      
        db.session.add(user)
        db.session.commit()
        return user
    
    def login_user(self, email, password):
        user = UserModel.query.filter_by(email=email).first()
        
        if not user:
            return {"Erro": "Usuário não encontrado!"}, 404
        
        if user.status != "Ativo":
            return {"Erro": "Usuário inativo, contate o administrador"}, 403

        if not check_password_hash(user.password, password):
            return {"Erro": "Senha inválida!"}, 401
        
        return user, 200
    
    def get_user(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return {"Erro": "Usuário não encontrado"}

        return user

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
    def delete_user(user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True