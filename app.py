from flask import Flask
from flask_restful import Api
from helpers.database import db, migrate
from helpers.confCors import cors
import os
from dotenv import load_dotenv

from resources.funcionarios import Funcionarios, FuncionarioId
from resources.enderecos import Enderecos, EnderecoId

load_dotenv()

postgresUser = os.getenv("POSTGRES_USER")
postgresPassword = os.getenv("POSTGRES_PASSWORD")

app = Flask(__name__)

DB_URL = f"postgresql://{postgresUser}:{postgresPassword}@localhost:5432/Educa365"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
cors.init_app(app)
migrate.__init__(app, db)
api = Api(app)

# Funcionarios - Resource
api.add_resource(Funcionarios, '/funcionarios')
api.add_resource(FuncionarioId, '/funcionarios/<string:id>')

# Enderecos - Resource
api.add_resource(Enderecos, '/enderecos')
api.add_resource(EnderecoId, '/enderecos/<id>')

if __name__ == '__main__':
  app.run(debug=True)