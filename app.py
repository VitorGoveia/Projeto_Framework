from flask import Flask
#Precisamos criar as rotas
#Precisamos criar a config do db

def create_app():
    """Função de criação e configuração do Flask"""

    app = Flask(__name__)

    #config db vai aqui
    #config rotas vai aqui

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)