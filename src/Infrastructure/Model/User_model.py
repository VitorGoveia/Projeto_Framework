from src.Config.db import db 

class UserModel(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Inativo')
    code = db.Column(db.Integer, nullable = True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "status": self.status
        }