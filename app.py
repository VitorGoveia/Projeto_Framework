from flask import Flask
from src.Config.db import init_db
from src.routes import register_routes

def create_app():
    app = Flask(__name__)

    # inicializa DB
    init_db(app)

    # registra rotas
    register_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)