from flask import Flask
from src.Config.db import init_db
from src.Domain.User import UserDomain
from src.Infrastructure.routes import register_routes

def create_app():
    app = Flask(__name__)

    # inicializa DB
    init_db(app)

    # registra rotas
    register_routes(app)

    return app
