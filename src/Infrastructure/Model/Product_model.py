from src.Config.db import db 

class ProductModel(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Ativo')
    url_image = db.Column(db.String(255), nullable=True)

    id_seller = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    seller = db.relationship("UserModel", backref="produtos") 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "id_seller": self.id_seller,
            "url_image": self.url_image
        }