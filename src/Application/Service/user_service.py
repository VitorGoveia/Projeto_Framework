'''#Aqui seria para cirar o usuario e já colocar a informação dele no banco de dados

from src.Config.db import db
#from src.Infrastructure.Model.User_model import User
from src.Domain.User import UserDomain
"""
class UserService:
    @staticmethod
    def create_user(name, email, password):
        new_user = UserDomain(name, email, password)
      
        'Professor recomendou colocar aqui no user, uma coluna no banco com o nome CODE, que seria o código que será enviado via WPP para o usuario quando ele criar a conta, e o status começa inativo'
          
        user = User(name=new_user.name, email=new_user.email, password=new_user.password)        
        db.session.add(user)
        db.session.commit()
        return user
"""

class UserService:
    @staticmethod
    def create_user(name, email, password, celular, cnpj):
        new_user = UserDomain(name, email, password, celular, cnpj)
        user = User(name=new_user.name, email=new_user.email, password=new_user.password, celular=new_user.celular, cnpj=new_user.cnpj)        
        db.session.add(user)
        db.session.commit()
        return user'''