from flask import request, jsonify, make_response, current_app
from src.Application.Service.sell_service import SellService


class SellController:
    @staticmethod
    def create_sell(current_user_id):

        try:
            form = request.form

            required = ["client", "price","quantity","id_product"]

            faltante = [f for f in required if f not in form or not form.get(f).strip()]
            if faltante:
                return make_response(jsonify({"erro":f"Faltando campos: {faltante}"}), 400)
            
            sell_data = {
                "client": form.get("client"),
                "price": float(form.get("price")),
                "quantity": int(form.get("quantity")),
                "id_product": int(form.get("id_product"))
            }

            result, status_code = SellService.create_sell(current_user_id, **sell_data)
            

            if status_code == 201:
                return make_response(jsonify({
                    "mensagem": "Venda realizada com sucesso!",
                    "venda": {
                        "id": result.id,
                        "client": result.client,
                        "price": result.price,
                        "quantity": result.quantity,
                        "status": result.status,
                        "id_seller": current_user_id,
                        "name_seller": result.seller.name if result.seller else None,
                        "id_product": result.id_product,
                        "name_product": result.product.name if result.product else None
                    }
                }), 201)
            
            return make_response(jsonify(result), status_code) 
            
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro interno do servidor: {e}"}), 500)



    @staticmethod
    def get_sell_by_id(sell_id, current_user_id):
        try:
            result, status_code = SellService.get_sell_by_id(sell_id, current_user_id)

            
            if status_code != 200:
                return make_response(jsonify(result), status_code)
        
            
            sell = result
            seller = sell.seller
            product = sell.product

            return make_response(jsonify({
                "venda": {
                    "id": sell.id,
                    "client": sell.client,
                    "price": sell.price,
                    "quantity": sell.quantity,
                    "status": sell.status,
                    "id_seller": current_user_id,
                    "name_seller": seller.name if seller else None,
                    "id_product": product.id if product else None,
                    "name_product": product.name if product else None
                }
            }), 200)
        except Exception as e:
            current_app.logger.exception(f"Erro ao buscar venda: {e}")
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)


    @staticmethod
    def get_sell_by_id_seller(current_user_id):
        try:
            sells, status_code = SellService.get_sell_by_id_seller(current_user_id)

            if status_code != 200:
                return make_response(jsonify(sells), status_code)

            vendas_formatadas = []
            for sell in sells:
                seller = sell.seller
                product = sell.product
                vendas_formatadas.append({
                    "id": sell.id,
                    "client": sell.client,
                    "price": sell.price,
                    "quantity": sell.quantity,
                    "status": sell.status,
                    "id_seller": current_user_id,
                    "name_seller": seller.name if seller else None,
                    "id_product": product.id if product else None,
                    "name_product": product.name if product else None
                })

            return make_response(jsonify(vendas_formatadas), 200)
        
        except Exception as e:
            current_app.logger.exception(f"Erro ao buscar venda do vendedor: {e}")
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)
        

    @staticmethod
    def update_sell_by_id(sell_id, current_user_id):
        try:
            form = request.form

            sell_data = {}
            if "client" in form and form.get("client").strip():
                sell_data["client"] = form.get("client")

            if "price" in form and form.get("price").strip():
                sell_data["price"] = float(form.get("price"))
                
            if "quantity" in form and form.get("quantity").strip():
                sell_data["quantity"] = int(form.get("quantity"))    
                
            if "id_product" in form and form.get("id_product").strip():
                sell_data["id_product"] = int(form.get("id_product"))
                    
            if not sell_data:
                return make_response(jsonify({"erro":"Nenhum dado enviado para atualização"}), 400)
                
            sell, status_code = SellService.update_sell(sell_id, current_user_id, **sell_data)

            if status_code != 200:
                return make_response(jsonify(sell), status_code)
            
            seller = sell.seller
            product = sell.product

            return make_response(jsonify({
                "mensagem": "Venda atualizada com sucesso!",
                "venda": {
                    "id": sell.id,
                    "client": sell.client,
                    "price": sell.price,
                    "quantity": sell.quantity,
                    "status": sell.status,
                    "id_seller": current_user_id,
                    "name_seller": seller.name if seller else None,
                    "id_product": product.id if product else None,
                    "name_product": product.name if product else None,
                    "estoque_atual_produto": product.quantity if product else None
                }
            }), 200)

        except Exception as e:
            current_app.logger.exception("Erro ao atualizar venda")
            return make_response(jsonify({"erro": f"Erro interno do servidor {e}"}), 500)
                

    @staticmethod
    def delete_sell(sell_id, current_user_id):
        try:
            sell, status_code = SellService.delete_sell(sell_id, current_user_id)
            if status_code != 200:
                return make_response(jsonify(sell), status_code)
            
            seller = sell.seller
            product = sell.product

            return make_response(jsonify({
            "mensagem": "Venda cancelada com sucesso!",
            "venda": {
                "id": sell.id,
                "client": sell.client,
                "price": sell.price,
                "quantity": sell.quantity,
                "status": sell.status,
                "id_seller": current_user_id,
                "name_seller": seller.name if seller else None,
                "id_product": product.id if product else None,
                "name_product": product.name if product else None,
                "estoque_atual_produto": product.quantity if product else None
            }
        }), 200)

        except Exception as e:
            current_app.logger.exception(f"Erro ao cancelar venda com ID {sell_id}: {e}")
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)
              
            

