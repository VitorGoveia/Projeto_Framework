class SellDomain:
    def __init__(self, name, price, quantity, id_seller, id_product):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.id_seller = id_seller
        self.id_product = id_product
        self.status = "Processando"
    
    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity:": self.quantity,
            "id_seller": self.id_seller,
            "id_product": self.id_product,
            "status": self.status
        }