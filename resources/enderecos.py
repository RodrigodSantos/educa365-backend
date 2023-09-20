from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

from model.endereco import Endereco, enderecoFields
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("rua", type=str, help="Rua não informado", required=True)
parser.add_argument("bairro", type=str, help="Bairro não informado", required=True)
parser.add_argument("numero", type=str, help="Numero não informado", required=True)
parser.add_argument("uf", type=str, help="Uf não informado", required=True)
parser.add_argument("cidade", type=str, help="Cidade não informada", required=True)
parser.add_argument("cep", type=str, help="Cep não informado", required=True)
parser.add_argument("telefone", type=str, help="Telefone não informado", required=True)
parser.add_argument("referencia", type=str, help="Referencia não informada", required=True)

class Enderecos(Resource):
    def get(self):
        enderecos = Endereco.query.all()

        logger.info("Enderecos listados com sucesso!")
        return marshal(enderecos, enderecoFields), 200

    def post(self):
        args = parser.parse_args()
        try:
            endereco = Endereco(
              args['rua'],
              args['bairro'],
              args['numero'],
              args['uf'],
              args['cidade'],
              args['cep'],
              args['telefone'],
              args['referencia']
              )

            db.session.add(endereco)
            db.session.commit()

            logger.info(f"Endereco de id: {endereco.id} criado com sucesso")
            return marshal(endereco, enderecoFields), 200

        except:
            logger.error("Erro ao cadastrar o Endereco")

            codigo = Message(2, "Erro ao cadastrar o Endereco")
            return marshal(codigo, msgFields), 400


class EnderecoId(Resource):
    def get(self, id):
        endereco = Endereco.query.get(id)

        if endereco is None:
            logger.error(f"Endereco de id: {id} não encontrado")

            codigo = Message(1, f"Endereco de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404

        logger.info(f"Endereco de id: {id} listado com sucesso!")
        return marshal(endereco, enderecoFields), 200

    def put(self, id):
        try:
            args = parser.parse_args()

            endereco = Endereco.query.get(id)

            if endereco is None:
                logger.error(f"Endereco de id: {id} não encontrado")

                codigo = Message(1, f"Endereco de id: {id} não encontrado")
                return marshal(codigo, msgFields), 404

            endereco.rua = args['rua']
            endereco.bairro = args['bairro']
            endereco.numero = args['numero']
            endereco.uf = args['uf']
            endereco.cep = args['cep']
            endereco.telefone = args['telefone']
            endereco.referencia = args['referencia']

            db.session.add(endereco)
            db.session.commit()

            logger.info(f"Endereco de id: {id} atualizado com sucesso!")
            return marshal(endereco, enderecoFields), 200

        except:
            logger.error("Error ao atualizar o Endereco")

            codigo = Message(2, "Error ao atualizar o Endereco")
            return marshal(codigo, msgFields), 400

    def delete(self, id):

        endereco = Endereco.query.get(id)

        if endereco is None:
            logger.error(f"Endereco de id: {id} não encontrado")

            codigo = Message(1, f"Endereco de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404

        db.session.delete(endereco)
        db.session.commit()

        logger.info(f"Endereco de id: {id} deletedo com sucesso")
        return []