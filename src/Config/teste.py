from flask import Flask
from db import db, init_db

app = Flask(__name__)

class UserDomain(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    celular = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Inativo')

init_db(app)


@app.route('/')
def home():
    try:
        novo_usuario = UserDomain(name="Joao",
                                  cnpj="9876543321-25",
                                  email="joao.vitor@aluno.faculdadeimpacta.com.br",
                                  celular='5511925847798',
                                  password='souotario@69'
                                  )
        db.session.add(novo_usuario)
        db.session.commit()
        return 'Usuario adicionado com Sucesso!'
        
    except Exception as e:
        return f"Not working :( {e}"

@app.route('/user')
def getUser():
    try:
        usuario = UserDomain.query.get(2)
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
