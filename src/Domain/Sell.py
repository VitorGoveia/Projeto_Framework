class SellDomain:
    def __init__(self, client, price, quantity, id_seller, id_product):
        self.client = client
        self.price = price
        self.quantity = quantity
        self.id_seller = id_seller
        self.id_product = id_product
        self.status = "VENDIDO"
    
    def to_dict(self):
        return {
            "client": self.client,
            "price": self.price,
            "quantity:": self.quantity,
            "id_seller": self.id_seller,
            "id_product": self.id_product,
            "status": self.status
        }