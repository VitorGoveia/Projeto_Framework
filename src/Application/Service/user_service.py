from src.Config.db import db
from src.Infrastructure.Model.User_model import UserModel
from src.Domain.User import UserDomain
from werkzeug.security import generate_password_hash, check_password_hash
from src.Infrastructure.Http.whats_app import send_whatsapp_code

class UserService:
    
    @staticmethod
    def _validar_dados_obrigatorios(data, campos_obrigatorios):
        """Valida se todos os campos obrigatórios estão presentes"""
        campos_faltantes = [campo for campo in campos_obrigatorios if campo not in data]
        if campos_faltantes:
            return False, {"erro": f"Campos obrigatórios faltando: {campos_faltantes}"}, 400
        return True, None, None

    @staticmethod
    def create_user(**user_data):
        """Cria usuário recebendo dados como dicionário"""
        try:
            # Campos obrigatórios
            campos_obrigatorios = ["name", "email", "password", "phone", "cnpj"]
            valido, erro, status = UserService._validar_dados_obrigatorios(user_data, campos_obrigatorios)
            if not valido:
                return erro, status
            
            # Verifica se email ou CNPJ já existem
            existing_user = UserModel.query.filter(
                (UserModel.email == user_data["email"]) | 
                (UserModel.cnpj == user_data["cnpj"])
            ).first()
            
            if existing_user:
                if existing_user.email == user_data["email"]:
                    return {"erro": "Email já cadastrado"}, 409
                return {"erro": "CNPJ já cadastrado"}, 409
            
            # Gera código e hash da senha
            import random
            activation_code = random.randint(1000, 9999)
            user_data["code"] = activation_code
            user_data["password"] = generate_password_hash(user_data["password"])
            
            # Cria usuário usando desempacotamento
            new_user = UserDomain(**user_data)
            user = UserModel(
                name=new_user.name,
                email=new_user.email,
                password=new_user.password,
                phone=new_user.phone,
                cnpj=new_user.cnpj,
                code=new_user.code
            )
            
            db.session.add(user)
            db.session.commit()
            
            return user, 201
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def login_user(**credentials):
        """Login recebendo credenciais como dicionário"""
        try:
            # Valida campos obrigatórios
            campos_obrigatorios = ["email", "password"]
            valido, erro, status = UserService._validar_dados_obrigatorios(credentials, campos_obrigatorios)
            if not valido:
                return erro, status
            
            user = UserModel.query.filter_by(email=credentials["email"]).first()
            
            if not user:
                return {"erro": "Email ou senha inválidos"}, 401
            
            if not check_password_hash(user.password, credentials["password"]):
                return {"erro": "Email ou senha inválidos"}, 401
            
            if user.status != "Ativo":
                return {"erro": "Usuário inativo. Faça a ativação da conta."}, 403
            
            return user, 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def get_user_by_id(user_id):
        """Mantém igual pois só recebe um parâmetro"""
        try:
            user = UserModel.query.get(user_id)
            if not user:
                return {"erro": "Usuário não encontrado"}, 404

            return {
                "id": user.id,
                "name": user.name,
                "cnpj": user.cnpj, 
                "email": user.email,
                "phone": user.phone,
                "status": user.status,
                "data_criacao": user.created_at.isoformat() if user.created_at else None
            }, 200
            
        except Exception as e:
            raise e

    @staticmethod
    def update_user(user_id, **update_data):
        """Atualiza usuário recebendo dados como dicionário"""
        try:
            user = UserModel.query.get(user_id)
            if not user:
                return {"erro": "Usuário não encontrado"}, 404
            
            # Verifica se email já existe em outro usuário
            if 'email' in update_data and update_data['email'] != user.email:
                existing_user = UserModel.query.filter_by(email=update_data['email']).first()
                if existing_user and existing_user.id != user_id:
                    return {"erro": "Email já está em uso por outro usuário"}, 409
            
            # Campos permitidos para atualização
            campos_permitidos = ['name', 'cnpj', 'email', 'phone', 'password']
            
            for campo in campos_permitidos:
                if campo in update_data:
                    if campo == 'password':
                        setattr(user, campo, generate_password_hash(update_data[campo]))
                    else:
                        setattr(user, campo, update_data[campo])
            
            db.session.commit()
            
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "status": user.status
            }, 200
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def activating_user(**activation_data):
        """Ativa usuário recebendo dados como dicionário"""
        try:
            campos_obrigatorios = ["code", "email", "user_id"]
            valido, erro, status = UserService._validar_dados_obrigatorios(activation_data, campos_obrigatorios)
            if not valido:
                return erro, status
            
            user = UserModel.query.get(activation_data["user_id"])
            if not user:
                return {"erro": "Usuário não encontrado"}, 404
            
            if user.email != activation_data["email"]:
                return {"erro": "Email não corresponde ao usuário"}, 400
            
            if str(activation_data["code"]) != str(user.code):
                return {"erro": "Código de ativação inválido"}, 400
            
            user.status = "Ativo"
            db.session.commit()

            return {
                "mensagem": "Usuário ativado com sucesso!",
                "usuario": {
                    "email": user.email, 
                    "nome": user.name,
                    "status": user.status
                }
            }, 200
            
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def delete_user(user_id):
        """Recebe somente um parâmetro, mantém igual"""
        try:
            user = UserModel.query.get(user_id)
            if not user:
                return {"erro": "Usuário não encontrado"}, 404
            
            user.status = "Inativo"
            db.session.commit()
            
            return {"mensagem": "Usuário inativado com sucesso"}, 200
            
        except Exception as e:
            db.session.rollback()
            raise e