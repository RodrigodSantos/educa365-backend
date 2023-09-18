from flask_restful import Resource, reqparse, marshal
from helpers.database import db

from model.funcionario import Funcionario, funcionarioFields
from model.pessoa import Pessoa

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("sexo", type=str, help="Sexo não informado", required=True)
parser.add_argument("rg", type=str, help="Rg não informado", required=False)
parser.add_argument("dataNascimento", type=str, help="Data de nascimento não informado", required=False)
parser.add_argument("email", type=str, help="Email não informado", required=False)
parser.add_argument("cargo", type=str, help="Cargo não informado", required=False)

class Funcionarios(Resource):
  def get(self):
    funcionarios = Funcionario.query.all()
    return marshal(funcionarios, funcionarioFields), 200
  
  def post(self):
    args = parser.parse_args()

    funcionario = Funcionario(
      args['nome'], 
      args['sexo'], 
      args['rg'], 
      args['dataNascimento'], 
      args['email'], 
      args['cargo']
      )

    db.session.add(funcionario)
    db.session.commit()

    return marshal(funcionario, funcionarioFields), 200
    