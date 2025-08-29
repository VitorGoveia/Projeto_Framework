#Criação da classe Seller

class SellerDomain:
    def __init__(self, name, email, password, CNPJ, phone):
        self.name = name
        self.email = email
        self.password = password
        self.CNPJ = CNPJ
        self.phone = phone
        self.status = "Inativo"
    
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "CNPJ": self.CNPJ,
            "phone": self.phone,
            "status": self.status
        }