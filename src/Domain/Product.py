class ProductDomain:
    def __init__(self, name, price, quantity, id_seller, url_image):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.id_seller = id_seller
        self.url_image = url_image
        self.status = "Ativo"
    
    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "id_seller": self.id_seller,
            "url_image": self.url_image
        }