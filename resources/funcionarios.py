from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

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

class FuncionarioId(Resource):
    def get(self, id):
      funcionario = Funcionario.query.get(id)
      return marshal(funcionario, funcionarioFields), 200
    
    def put(self, id):
        args = parser.parse_args()

        funcionario = Funcionario.query.get(id)

        funcionario.nome = args['nome'], 
        funcionario.sexo = args['sexo'], 
        funcionario.rg= args['rg'], 
        funcionario.dataNascimento = args['dataNascimento'], 
        funcionario.email = args['email'], 
        funcionario.cargo = args['cargo']

        db.session.add(funcionario)
        db.session.commit()

        return marshal(funcionario, funcionarioFields), 200
    
    def delete(self, id):
        
        funcionario = Funcionario.query.get(id)

        db.session.delete(funcionario)
        db.session.commit()

        return []