from src.Config.db import db
from src.Infrastructure.Model.Sell_model import SellModel
from src.Infrastructure.Model.Product_model import ProductModel
from src.Domain.Sell import SellDomain

class SellService:
    @staticmethod
    def _validar_dados_obrigatorios(data, campos_obrigatorios):
        campos_faltantes = [campo for campo in campos_obrigatorios if campo not in data]
        if campos_faltantes:
            return False, {"erro": f"Campos obrigatórios faltando: {campos_faltantes}"}, 400
        return True, None, None

    @staticmethod
    def create_sell(**sell_data):
        try:
            campos_obrigatorios = ["price", "quantity", "id_seller", "id_product"]
            valido, erro, status = SellService._validar_dados_obrigatorios(sell_data, campos_obrigatorios)
            if not valido:
                return erro, status
            
            product = ProductModel.query.get(sell_data["id_product"])
            if not product:
                return {"erro": "Produto não encontrado"}, 404
            
            if product.status != "Ativo":
                return {"erro": "Produto inativo"}, 400
            
            if product.quantity < sell_data["quantity"]:
                return {"erro": f"Quantidade insuficiente em estoque. Disponível: {product.quantity}"}, 400
            
            product.quantity -= sell_data["quantity"]
            
            new_sell = SellDomain(**sell_data)
            
            sell = SellModel(
                price=new_sell.price,
                quantity=new_sell.quantity,
                id_seller=new_sell.id_seller,
                id_product=new_sell.id_product,
                status=new_sell.status
            
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
                return {"erro": "Você não tem permissão para acessar esta venda"}, 403
            
            return sell.to_dict(), 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def get_sell_by_id_seller(id_seller):
        try:
            sells = SellModel.query.filter_by(id_seller=id_seller).all()
            if not sells:
                return {"mensagem": "Nenhuma venda encontrada"}, 200
            
            return [sell.to_dict() for sell in sells], 200
            
        except Exception as e:
            raise e
    
    @staticmethod
    def update_sell(sell_id, current_user_id, **update_data):
        try:
            sell = SellModel.query.get(sell_id)
            if not sell:
                return {"erro": "Venda não encontrada"}, 404
            
            if sell.id_seller != current_user_id:
                return {"erro": "Você não tem permissão para atualizar esta venda"}, 403
            
            campos_permitidos = ['client', 'price', 'quantity', 'status']
            
            if 'quantity' in update_data and update_data['quantity'] != sell.quantity:
                product = ProductModel.query.get(sell.id_product)
                if not product:
                    return {"erro": "Produto associado não encontrado"}, 404
                
                diferenca = update_data['quantity'] - sell.quantity
                
                if diferenca > 0:
                    if product.quantity < diferenca:
                        return {"erro": f"Quantidade insuficiente em estoque. Disponível: {product.quantity}"}, 400
                    product.quantity -= diferenca
                else:
                    product.quantity += abs(diferenca)
            
            for campo in campos_permitidos:
                if campo in update_data:
                    setattr(sell, campo, update_data[campo])
            
            db.session.commit()
            
            return sell.to_dict(), 200
            
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
                return {"erro": "Você não tem permissão para cancelar esta venda"}, 403
            
            product = ProductModel.query.get(sell.id_product)
            if product:
                product.quantity += sell.quantity
            
            sell.status = "CANCELADO"
            db.session.commit()
            
            return {"mensagem": "Venda cancelada com sucesso"}, 200
            
        except Exception as e:
            db.session.rollback()
            raise e