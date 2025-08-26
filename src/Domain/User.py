#Criação da classe usuario
#Nome
#CNPJ
#E-mail
#Celular
#Senha
#Status (Padrão: Inativo)

from Config.db import db 

class UserDomain(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    celular = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Inativo')