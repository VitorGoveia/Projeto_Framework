class SellDomain:
    def __init__(self, cliente, price, quantity, id_seller, id_product):
        self.cliente = cliente
        self.price = price
        self.quantity = quantity
        self.id_seller = id_seller
        self.id_product = id_product
        self.status = "Ativa"
    
    def to_dict(self):
        return {
            "cliente": self.cliente,
            "price": self.price,
            "quantity:": self.quantity,
            "id_seller": self.id_seller,
            "id_product": self.id_product,
            "status": self.status
        }