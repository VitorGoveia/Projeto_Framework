from flask import request, jsonify, make_response
from src.Application.Service.sell_service import SellService

class SellController:
    @staticmethod
    def create_sell(current_user_id):
        try:
            data = request.get_json()
            
            if not data:
                return make_response(jsonify({"erro": "Dados JSON são obrigatórios"}), 400)
            
            dados_obrigatorios = ["price", "quantity", "id_product"]
            info_faltantes = [item for item in dados_obrigatorios if item not in data]
            
            if info_faltantes:
                return make_response(
                    jsonify({"erro": f"Estão faltando os seguintes campos: {info_faltantes}"}), 
                    400
                )
            
            # Adiciona o id_seller do usuário autenticado
            data["id_seller"] = current_user_id
            
            result, status_code = SellService.create_sell(**data)
            
            if status_code != 201:
                return make_response(jsonify(result), status_code)
            
            return make_response(jsonify({
                "mensagem": "Venda criada com sucesso",
                "venda": result.to_dict()
            }), 201)
            
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)
    
    @staticmethod
    def get_sell_by_id(sell_id, current_user_id):
        try:
            result, status_code = SellService.get_sell_by_id(sell_id, current_user_id)
            return make_response(jsonify(result), status_code)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)
    
    @staticmethod
    def get_sell_by_id_seller(current_user_id):
        try:
            result, status_code = SellService.get_sell_by_id_seller(current_user_id)
            return make_response(jsonify(result), status_code)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)
    
    @staticmethod
    def update_sell_by_id(sell_id, current_user_id):
        try:
            data = request.get_json()
            
            if not data:
                return make_response(jsonify({"erro": "Dados JSON são obrigatórios"}), 400)
            
            result, status_code = SellService.update_sell(sell_id, current_user_id, **data)
            return make_response(jsonify(result), status_code)
            
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)
    
    @staticmethod
    def delete_sell(sell_id, current_user_id):
        try:
            result, status_code = SellService.delete_sell(sell_id, current_user_id)
            return make_response(jsonify(result), status_code)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)