from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger
from sqlalchemy.exc import IntegrityError

import datetime

from model.funcionario import Funcionario, funcionarioFields
from model.mensagem import Message, msgFields
from model.endereco import Endereco
from model.pessoa import Pessoa

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("sexo", type=str, help="Sexo não informado", required=True)
parser.add_argument("rg", type=str, help="Rg não informado", required=False)
parser.add_argument("cpf", type=str, help="Cpf não informado", required=False)
parser.add_argument("dataNascimento", type=str, help="Data de nascimento não informada", required=False)
parser.add_argument("email", type=str, help="Email não informado", required=False)
parser.add_argument("cargo", type=str, help="Cargo não informado", required=False)
parser.add_argument("senha", type=str, help="Senha não informada", required=False)
parser.add_argument("endereco", type=dict, help="Endereço não informado", required=False)

class Funcionarios(Resource):
    def get(self):
        funcionarios = Funcionario.query.all()

        logger.info("Funcionarios listados com sucesso!")
        return marshal(funcionarios, funcionarioFields), 200
    
    def post(self):
        args = parser.parse_args()
        try:
            endereco = Endereco.query.get(args['endereco'])
            dataNascimento = args['dataNascimento'].split('-')
            dataNascimento = datetime.datetime(
                year=int(dataNascimento[0]), 
                month=int(dataNascimento[1]), 
                day=int(dataNascimento[2])
                )

            funcionario = Funcionario(
                args['nome'], 
                args['sexo'], 
                args['rg'],
                args['cpf'],
                dataNascimento, 
                args['email'], 
                args['cargo'],
                args['senha'],
                endereco
                )

            db.session.add(funcionario)
            db.session.commit()

            logger.info(f"Funcionario de id: {funcionario.id} criado com sucesso")
            return marshal(funcionario, funcionarioFields), 200
        
        except IntegrityError:
            logger.error("Erro ao cadastrar o Funcionario - Email, cpf ou rg ja cadastrado no sistema")

            codigo = Message(1, "Erro ao cadastrar o Funcionario - Email, cpf ou rg ja cadastrado no sistema")
            return marshal(codigo, msgFields)
        
        except:
          
          logger.error("Erro ao cadastrar o Funcionario")

          codigo = Message(2, "Erro ao cadastrar o Funcionario")
          return marshal(codigo, msgFields), 400
        

class FuncionarioId(Resource):
    def get(self, id):
        funcionario = Funcionario.query.get(id)

        if funcionario is None:
            logger.error(f"Funcionario de id: {id} não encontrado")

            codigo = Message(1, f"Funcionario de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404
            
        logger.info(f"Funcionario de id: {id} listado com sucesso!")
        return marshal(funcionario, funcionarioFields), 200
    
    def put(self, id):
        try:
            args = parser.parse_args()
            endereco = Endereco.query.get(args['endereco'])
            funcionario = Funcionario.query.get(id)

            if funcionario is None:
                logger.error(f"Funcionario de id: {id} não encontrado")

                codigo = Message(1, f"Funcionario de id: {id} não encontrado")
                return marshal(codigo, msgFields), 404

            funcionario.nome = args['nome']
            funcionario.sexo = args['sexo']
            funcionario.rg = args['rg']
            funcionario.cpf = args['cpf']
            funcionario.dataNascimento = args['dataNascimento']
            funcionario.email = args['email']
            funcionario.cargo = args['cargo']
            funcionario.senha = args['senha']
            funcionario.endereco = endereco


            db.session.add(funcionario)
            db.session.commit()

            logger.info(f"Funcionario de id: {id} atualizado com sucesso!")
            return marshal(funcionario, funcionarioFields), 200
        
        except IntegrityError:
            logger.error("Erro ao atualizar o email do Funcionario - Email pertence a outro usuário")

            codigo = Message(1, "Erro ao atualizar o email do Funcionario - Email pertence a outro usuário")
            return marshal(codigo, msgFields)
        
        except:
          logger.error("Error ao atualizar o Funcionario")

          codigo = Message(2, "Error ao atualizar o Funcionario")
          return marshal(codigo, msgFields), 400
            
    
    def delete(self, id):
        
        funcionario = Funcionario.query.get(id)

        if funcionario is None:
            logger.error(f"Funcionario de id: {id} não encontrado")

            codigo = Message(1, f"Funcionario de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404

        logger.info(f"Funcionario de id: {id} deletado com sucesso!")
        db.session.delete(funcionario)
        db.session.commit()

        return []