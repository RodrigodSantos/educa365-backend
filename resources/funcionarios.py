from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger
from sqlalchemy.exc import IntegrityError

import datetime
import uuid

from model.funcionario import Funcionario, funcionarioFields
from model.mensagem import Message, msgFields
from model.endereco import Endereco
from model.pessoa import Pessoa

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("sexo", type=bool, help="Sexo não informado", required=True)
parser.add_argument("rg", type=str, help="Rg não informado", required=True)
parser.add_argument("cpf", type=str, help="Cpf não informado", required=True)
parser.add_argument("dataNascimento", type=str, help="Data de nascimento não informada", required=True)
parser.add_argument("email", type=str, help="Email não informado", required=True)
parser.add_argument("cargo", type=str, help="Cargo não informado", required=True)
parser.add_argument("senha", type=str, help="Senha não informada", required=False)
parser.add_argument("endereco", type=dict, help="Endereço não informado", required=True)

class Funcionarios(Resource):
    def get(self):
        funcionarios = Funcionario.query.all()

        logger.info("Funcionarios listados com sucesso!")
        return marshal(funcionarios, funcionarioFields), 200

    def post(self):
        args = parser.parse_args()
        try:
            dataNascimento = args['dataNascimento'].split('-')
            dataNascimento = datetime.datetime(
                year=int(dataNascimento[0]),
                month=int(dataNascimento[1]),
                day=int(dataNascimento[2])
                )

            endereco = Endereco(
                args['endereco']['rua'],
                args['endereco']['bairro'],
                args['endereco']['numero'],
                args['endereco']['uf'],
                args['endereco']['cidade'],
                args['endereco']['cep'],
                args['endereco']['telefone'],
                args['endereco']['referencia']
            )

            db.session.add(endereco)
            db.session.commit()
            logger.info(f"Endereco de id: {endereco.id} criado com sucesso")

            funcionario = Funcionario(
                args['nome'],
                args['sexo'],
                args['rg'],
                args['cpf'],
                dataNascimento,
                endereco,
                args['email'],
                args['cargo'],
                args['senha']
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
        funcionario = Funcionario.query.get(uuid.UUID(int=id))

        if funcionario is None:
            logger.error(f"Funcionario de id: {id} não encontrado")

            codigo = Message(1, f"Funcionario de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404

        logger.info(f"Funcionario de id: {id} listado com sucesso!")
        return marshal(funcionario, funcionarioFields), 200

    def put(self, id):
        try:
            args = parser.parse_args()

            funcionario = Funcionario.query.get(uuid.UUID(int=id))

            if funcionario is None:
                logger.error(f"Funcionario de id: {id} não encontrado")

                codigo = Message(1, f"Funcionario de id: {id} não encontrado")
                return marshal(codigo, msgFields), 404

            endereco = Endereco.query.get(funcionario.endereco.id)

            endereco.rua = args['endereco']['rua']
            endereco.bairro = args['endereco']['bairro']
            endereco.numero = args['endereco']['numero']
            endereco.uf = args['endereco']['uf']
            endereco.cidade = args['endereco']['cidade']
            endereco.cep = args['endereco']['cep']
            endereco.telefone = args['endereco']['telefone']
            endereco.referencia = args['endereco']['referencia']

            db.session.add(endereco)
            db.session.commit()

            funcionario.nome = args['nome']
            funcionario.sexo = args['sexo']
            funcionario.rg = args['rg']
            funcionario.cpf = args['cpf']
            funcionario.dataNascimento = args['dataNascimento']
            funcionario.endereco = endereco
            funcionario.email = args['email']
            funcionario.cargo = args['cargo']
            funcionario.senha = args['senha']


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

        funcionario = Funcionario.query.get(uuid.UUID(int=id))

        if funcionario is None:
            logger.error(f"Funcionario de id: {id} não encontrado")

            codigo = Message(1, f"Funcionario de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404

        logger.info(f"Funcionario de id: {id} deletado com sucesso!")
        db.session.delete(funcionario)
        db.session.commit()

        return []
