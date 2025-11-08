from src.Config.db import db
from src.Infrastructure.Model.Sell_model import SellModel
from src.Domain.Sell import SellDomain
from src.Infrastructure.Model.Product_model import ProductModel
from src.Infrastructure.Model.User_model import UserModel

class SellService:
    @staticmethod
    def _validar_dados_obrigatorios(data, campos_obrigatorios):
        campos_faltantes = [campo for campo in campos_obrigatorios if campo not in data]
        if campos_faltantes:
            return False, {"erro": f"Campos obrigatórios faltando: {campos_faltantes}"}, 400
        return True, None, None
    

    @staticmethod
    def create_sell(current_user_id,**sell_data):
        try:
    
            sell_data["id_seller"] = current_user_id

            campos_obrigatorios = ["client", "price", "quantity", "id_product"]
            valido, erro, status = SellService._validar_dados_obrigatorios(sell_data, campos_obrigatorios)
            if not valido:
                return erro, status
            

            product = ProductModel.query.get(sell_data["id_product"])
            seller = UserModel.query.get(sell_data["id_seller"])
            quantity = sell_data["quantity"]

            if not product:
                return {"erro": "Produto não encontrado."}, 404

            if not seller:
                return {"erro": "Seller não encontrado."}, 404

            if not product.status:
                return {"erro": "Produto inativo, não pode ser vendido."}, 400

            if not seller.status:
                return {"erro": "Seller inativo, não pode realizar vendas."}, 400

            if quantity > product.quantity:
                return {"erro": "Quantidade solicitada excede o estoque disponível."}, 400
            product.quantity -= quantity
            
            new_sell = SellDomain(**sell_data)
            sell = SellModel(
                client=new_sell.client,
                price=new_sell.price,
                quantity=new_sell.quantity,
                id_seller=current_user_id,
                id_product=new_sell.id_product
            )
            
            db.session.add(sell)
            db.session.commit()

            return sell, 201

        
        except Exception as e:
            db.session.rollback()
            raise e
        

    @staticmethod
    def get_sell_by_id(sell_id, current_user_id):
        try:
            sell = SellModel.query.get(sell_id)
            if not sell:
                return {"erro": "Venda não encontrada"}, 404
            if sell.id_seller != current_user_id:
                return {"erro": "Acesso negado"}, 403
        
            return sell, 200  
        except Exception as e:
            raise e


    @staticmethod
    def get_sell_by_id_seller(current_user_id):
        try:
            sells = SellModel.query.filter_by(id_seller=current_user_id).all()
            if not sells:
                return {"erro": "Vendas não encontradas"}, 404
        
            return sells, 200  
        except Exception as e:
            raise e


    @staticmethod
    def update_sell(sell_id, current_user_id, **update_data):
        try:
            sell = SellModel.query.get(sell_id)
            if not sell:
                return {"erro":"Venda não encontrada"}, 404
        
            if sell.id_seller != current_user_id:
                return {"erro": "Não autorizado"}, 403

            campos_obrigatorios = ["client", "price", "quantity", "id_product"]
            valido, erro, status = SellService._validar_dados_obrigatorios(update_data, campos_obrigatorios)
            if not valido:
                return erro, status
        
            product = ProductModel.query.get(update_data["id_product"])
        
            if not product:
                return {"erro": "Produto referente à venda não encontrado"}, 404
        
            # AJUSTE DE ESTOQUE
            diferenca = update_data["quantity"] - sell.quantity

            if diferenca > 0:
                if product.quantity < diferenca:
                    return {"erro": "Estoque insuficiente para aumentar a quantidade da venda"}, 400
                product.quantity -= diferenca
            elif diferenca < 0:
                product.quantity += abs(diferenca)
        
            sell.client = update_data["client"]
            sell.price = update_data["price"]
            sell.quantity = update_data["quantity"]
            sell.id_product = update_data["id_product"]

            db.session.commit()

            return sell, 200  
    
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def delete_sell(sell_id, current_user_id):
        try:
            sell = SellModel.query.get(sell_id)
            if not sell:
                return {"erro": "Venda não encontrada"}, 404
        
            if sell.id_seller != current_user_id:
                return {"erro": "Não autorizado"}, 403
        
            if sell.status == "Cancelada":  
                return {"erro": "Venda já está cancelada"}, 400

            product = ProductModel.query.get(sell.id_product)
            if not product:
                return {"erro": "Produto referente à venda não encontrado"}, 404

            product.quantity += sell.quantity
            sell.status = "Cancelada"  

            db.session.commit()

            return sell, 200

        except Exception as e:
            db.session.rollback()
            raise e


