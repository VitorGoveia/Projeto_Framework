class UserDomain:
    def __init__(self, name, email, password, CNPJ, phone, code):
        self.name = name
        self.email = email
        self.password = password
        self.CNPJ = CNPJ
        self.phone = phone
        self.status = "Inativo"
        self.code = code
    
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "CNPJ": self.CNPJ,
            "phone": self.phone,
            "status": self.status,
            "code": self.code
        }