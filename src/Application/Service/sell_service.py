from src.Config.db import db
from src.Infrastructure.Model.Sell_model import SellModel
from src.Domain.Sell import SellDomain

class SellService:
    @staticmethod
    def _validar_dados_obrigatorios(data, campos_obrigatorios):
        campos_faltantes = [campo for campo in campos_obrigatorios if campo not in data]
        if campos_faltantes:
            return False, {"erro": f"Campos obrigatórios faltando: {campos_faltantes}"}
        return True, None, None
    

    @staticmethod
    def create_sell(**sell_data):
        try:
            campos_obrigatorios = ["cliente", "price", "quantity", "id_seller", "id_product"]
            valido, erro, status = SellService._validar_dados_obrigatorios(sell_data, campos_obrigatorios)
            if not valido:
                return erro, status
            
            new_sell = SellDomain(**sell_data)
            sell = SellDomain(
                cliente=new_sell.cliente,
                price=new_sell.price,
                quantity=new_sell.quantity,
                id_seller=new_sell.id_seller,
                id_product=new_sell.id_product
            )

            db.session.add(sell)
            db.session.commit()

            return sell, 201
        
        except Exception as e:
            db.session.rollback()
            raise e
        

    @staticmethod
    def get_sell_by_id(sell_id):
        try:
            sell = SellModel.query.get(sell_id)
            if not sell:
                return {"erro":"Venda não encontrada"}, 404
            
            if sell.status == False:
                return {"erro":"Venda inativa"}, 404
            
            return sell.to_dict(), 200
        
        except Exception as e:
            raise e
        
    @staticmethod
    def get_sell_by_id_seller(id_seller_info):
        try:
            sell = SellModel.query.filter_by(id_seller=id_seller_info).all()
            if not sell:
                return {"erro":"Venda não encontrada"}, 404
            
            return [venda.to_dict() for venda in sell] , 200
        
        except Exception as e:
            raise e
    
    @staticmethod
    def update_sell(sell_id, **update_data):
        try:
            sell = SellModel.query.get(sell_id)
            if not sell:
                return {"erro":"Venda não encontrada"}, 404

            campos_obrigatorios = ["cliente", "price", "quantity", "id_seller", "id_product", "status"]

