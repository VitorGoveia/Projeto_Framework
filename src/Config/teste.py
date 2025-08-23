from flask import Flask
from db import db, init_db

app = Flask(__name__)


class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

init_db(app)

@app.route('/')
def home():
    try:
        novo_usuario = User(name="Gustavo", email="gustavo.gozzi@aluno.faculdadeimpacta.com.br")
        db.session.add(novo_usuario)
        db.session.commit()
        return 'Usuario adicionado com Sucesso!'
        
    except Exception as e:
        return f"Not working :( {e}"

@app.route('/user')
def getUser():
    try:
        usuario = User.query.get(1)
        user = {
            'id': usuario.id,
            'nome': usuario.name,
            'email': usuario.email
        }
        return user
    
    except Exception as e:
        return f'Deu ruim {e}'


if __name__ == '__main__':
    app.run(debug=True)
