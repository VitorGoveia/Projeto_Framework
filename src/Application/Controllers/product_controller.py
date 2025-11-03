from flask import request, jsonify, make_response, current_app
from src.Application.Service.product_service import ProductService
from werkzeug.utils import secure_filename
import os
import uuid

class ProductController:
    @staticmethod
    def register_product():
        UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static', 'images')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        try:
            form = request.form
            file = request.files.get('url_image')  

            required = ["name", "price", "quantity", "id_seller"]

            faltante = [f for f in required if f not in form or not form.get(f).strip()]
            if faltante and not file:
                return make_response(jsonify({"erro": f"Faltando campos: {faltante}"}), 400)

            if not file:
                return make_response(jsonify({"erro": "Nenhum arquivo de imagem enviado"}), 400)

            if file.filename == "":
                return make_response(jsonify({"erro": "Nome de arquivo inválido"}), 400)

            filename = secure_filename(file.filename)
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(file_path)

            image_url = f"/static/images/{unique_name}"

            product_data = {
                "name": form.get("name"),
                "price": float(form.get("price")),
                "quantity": int(form.get("quantity")),
                "id_seller": int(form.get("id_seller")),
                "url_image": image_url
            }

            result, status_code = ProductService.create_product(**product_data)

            if status_code != 201:
                return make_response(jsonify(result), status_code)

            return make_response(jsonify({
                "mensagem": "Produto criado com sucesso",
                "produto": result.to_dict()
            }), 201)

        except Exception as e:
            return make_response(jsonify({"erro": f"Erro interno do servidor: {e}"}), 500)
            
    @staticmethod
    def get_product(product_id):
        """Busca usuário por ID"""
        try:
            result, status_code = ProductService.get_product_by_id(product_id)
            return make_response(jsonify(result), status_code)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)
    
    @staticmethod
    def update_product(product_id):
        UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static', 'images')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        try:
            form = request.form
            file = request.files.get('url_image')  

            product_data = {}
            if "name" in form and form.get("name").strip():
                product_data["name"] = form.get("name")
            if "price" in form and form.get("price").strip():
                product_data["price"] = float(form.get("price"))
            if "quantity" in form and form.get("quantity").strip():
                product_data["quantity"] = int(form.get("quantity"))
            if "id_seller" in form and form.get("id_seller").strip():
                product_data["id_seller"] = int(form.get("id_seller"))
            if "status" in form and form.get("id_seller").strip():
                validar = form.get("id_seller")
                if validar in "AtivoativoATIVO":
                    product_data["status"] = "Ativo"
                else:
                    product_data["status"] = "Inativo"

            if file and file.filename:
                filename = secure_filename(file.filename)
                unique_name = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_name)
                file.save(file_path)
                product_data["url_image"] = f"/static/images/{unique_name}"

            if not product_data:
                return make_response(jsonify({"erro": "Nenhum dado enviado para atualização"}), 400)

            result, status_code = ProductService.update_product(product_id, **product_data)

            return make_response(jsonify(result), status_code)

        except Exception as e:
            current_app.logger.exception("Erro ao atualizar produto")
            return make_response(jsonify({"erro": f"Erro interno do servidor: {e}"}), 500)
    
    @staticmethod
    def delete_product(product_id):
        try:
            result, status_code = ProductService.delete_product(product_id)
            return make_response(jsonify(result), status_code)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)