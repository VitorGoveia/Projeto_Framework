from flask_sqlalchemy import SQLAlchemy
import psycopg2

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@db:5432/mamutedb' # postgres:2400779@localhost // usuario:senha@db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()



''' Testei e isso realmente nao parece ser necessario
def create_Dabase_if_not_exists():
    try:
        conector = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="240052",
            host="localhost",
            port="5432"
        )
        conector.autocommit = True
        cur = conector.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'mamutedb'")
        exists = cur.fetchone()
        if not exists:
            cur.execute('CREATE DATABASE mamutedb')
            print("Banco criado com Sucesso!")
        
        else: print("Banco já existe!")
        
        cur.close()
        conector.close()

    except Exception as e:
        print("Erro ao criar banco:", e)

'''