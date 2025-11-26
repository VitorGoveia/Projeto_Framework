class SellDomain:
    def __init__(self, price, quantity, id_seller, id_product):
        self.price = price
        self.quantity = quantity
        self.id_seller = id_seller
        self.id_product = id_product
        self.status = "VENDIDO"
        self.isactivate = True
    
    def to_dict(self):
        return {
            "price": self.price,
            "quantity": self.quantity,
            "id_seller": self.id_seller,
            "id_product": self.id_product,
            "status": self.status,
            "isactivate": self.isactivate
        }