from src.Config.db import db


class SellModel(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Processando')

    id_seller = db.Column(db.Column)(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    seller = db.relationship("UserModel", backref="vendas")

    id_product = (db.Column)(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    product = db.relationship("ProductModel", backref="vendas")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "id_seller": self.id_seller,
            "id_product": self.id_product
        }