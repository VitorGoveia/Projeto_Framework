class UserDomain:
    def __init__(self, name, email, password, phone, cnpj): #add ',code' depois de phone
        self.name = name
        self.email = email
        self.password = password
        self.cnpj = cnpj
        self.phone = phone
        self.status = "Inativo"
        self.code = 1234
    
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "cnpj": self.cnpj,
            "phone": self.phone,
            "status": self.status,
            "code": self.code
        }