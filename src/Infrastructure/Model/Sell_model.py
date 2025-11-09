from src.Config.db import db
from datetime import datetime


class SellModel(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='VENDIDO')
    data_venda = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    id_seller = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    seller = db.relationship("UserModel", backref="vendas")
    
    id_product = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    product = db.relationship("ProductModel", backref="vendas")

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "data_venda": self.data_venda.strftime('%d/%m/%Y %H:%M:%S') if self.data_venda else None,
            "id_seller": self.id_seller,
            "seller_name": self.seller.name if self.seller else None,
            "id_product": self.id_product,
            "product_name": self.product.name if self.product else None
        }