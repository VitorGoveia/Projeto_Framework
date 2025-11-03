from src.Config.db import db
from src.Infrastructure.Model.Product_model import ProductModel
from src.Domain.Product import ProductDomain

class ProductService:
    @staticmethod
    def _validar_dados_obrigatorios(data, campos_obrigatorios):
        campos_faltantes = [campo for campo in campos_obrigatorios if campo not in data]
        if campos_faltantes:
            return False, {"erro": f"Campos obrigatórios faltando: {campos_faltantes}"}, 400
        return True, None, None

    @staticmethod
    def create_product(**product_data):
        try:
            campos_obrigatorios = ["name", "price", "quantity", "id_seller", "url_image"]
            valido, erro, status = ProductService._validar_dados_obrigatorios(product_data, campos_obrigatorios)
            if not valido:
                return erro, status
            
            new_product = ProductDomain(**product_data)
            product = ProductModel(
                name=new_product.name,
                price=new_product.price,
                quantity=new_product.quantity,
                id_seller=new_product.id_seller,
                url_image=new_product.url_image
            )
            
            db.session.add(product)
            db.session.commit()
            
            return product, 201
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_product_by_id(product_id):
        try:
            product = ProductModel.query.get(product_id)
            if not product:
                return {"erro": "Produto não encontrado"}, 404

            return product.to_dict(), 200
            
        except Exception as e:
            raise e

    @staticmethod
    def update_product(product_id, **update_data):
        try:
            product = ProductModel.query.get(product_id)
            if not product:
                return {"erro": "Produto não encontrado"}, 404
            
            campos_obrigatorios = ["name", "price", "quantity", "id_seller", "url_image", "status"]
            valido, erro, status = ProductService._validar_dados_obrigatorios(update_data, campos_obrigatorios)
            if not valido:
                return erro, status
            
            product.name = update_data["name"]
            product.price = update_data["price"]
            product.quantity = update_data["quantity"]
            product.id_seller = update_data["id_seller"]
            product.status = update_data["status"]
            product.url_image = update_data["url_image"]

            db.session.commit()
            
            return product.to_dict(), 200
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_product(product_id):
        try:
            product = ProductModel.query.get(product_id)
            if not product:
                return {"erro": "Usuário não encontrado"}, 404
            
            product.status = "Inativo"
            db.session.commit()
            
            return {"mensagem": "Produto inativado com sucesso"}, 200
            
        except Exception as e:
            db.session.rollback()
            raise e