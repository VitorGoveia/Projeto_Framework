from flask import Flask
from db import db, init_db
from Domain.User import UserDomain

app = Flask(__name__)


init_db(app)

@app.route('/')
def home():
    try:
        novo_usuario = UserDomain(name="Gustavo",
                                  cnpj="123456789-1011",
                                  email="gustavo.gozzi@aluno.faculdadeimpacta.com.br",
                                  celular='5511912345678',
                                  password='147896352@'
                                  )
        db.session.add(novo_usuario)
        db.session.commit()
        return 'Usuario adicionado com Sucesso!'
        
    except Exception as e:
        return f"Not working :( {e}"

@app.route('/user')
def getUser():
    try:
        usuario = UserDomain.query.get(1)
        user = {
            'id': usuario.id,
            'nome': usuario.name,
            'email': usuario.email,
            'celular': usuario.celular,
            'status': usuario.status
        }
        return user
    
    except Exception as e:
        return f'Deu ruim {e}'


if __name__ == '__main__':
    app.run(debug=True)
