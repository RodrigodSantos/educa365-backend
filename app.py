from flask import Flask
from flask_restful import Api
from helpers.database import db, migrate
from helpers.confCors import cors

from resources.funcionarios import Funcionarios

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:senha@localhost:5432/Educa365"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
cors.init_app(app)
migrate.__init__(app, db)
api = Api(app)

api.add_resource(Funcionarios, '/funcionarios')

if __name__ == '__main__':
  app.run(debug=True)