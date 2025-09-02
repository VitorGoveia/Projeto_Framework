from flask import jsonify
from src.Domain.User import UserDomain
from src.Config.db import db

def register_routes(app):
    @app.route('/')
    def home():
        try:
            novo_usuario = UserDomain(
                name="Joao",
                cnpj="9876543321-25",
                email="joao.vitor@aluno.faculdadeimpacta.com.br",
                celular="5511925847798",
                password="souotario@69"
            )
            db.session.add(novo_usuario)
            db.session.commit()
            return 'Usuario adicionado com Sucesso!'
        except Exception as e:
            return f"Not working :( {e}"

    @app.route('/user')
    def get_user():
        try:
            usuario = UserDomain.query.get(2)
            if not usuario:
                return jsonify({"erro": "Usuário não encontrado"}), 404

            return {
                'id': usuario.id,
                'nome': usuario.name,
                'email': usuario.email,
                'celular': usuario.celular,
                'status': usuario.status
            }
        except Exception as e:
            return f'Deu ruim {e}'
