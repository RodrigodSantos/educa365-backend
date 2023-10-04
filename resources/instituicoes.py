from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.instituicaoEnsino import InstituicaoEnsino, instituicaoEnsinoFields
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("cnpj", type=str, help="Cnpj não informado", required=True)

class Instituicoes(Resource):
    def get(self):
        instituicao = InstituicaoEnsino.query.all()

        logger.info("Instituicoes listados com sucesso!")
        return marshal(instituicao, instituicaoEnsinoFields), 200

    def post(self):
        try:
            args = parser.parse_args()

            instituicao = InstituicaoEnsino(
                args['nome'],
                args['cnpj']
            )

            db.session.add(instituicao)
            db.session.commit()

            logger.info(f"Instituicao de Ensino de id: {instituicao.id} criado com sucesso")
            return marshal(instituicao, instituicaoEnsinoFields)

        except:
            logger.error("Erro ao cadastrar a Instituicao de Ensino")

            codigo = Message(2, "Erro ao cadastrar a Instituicao de Ensino")
            return marshal(codigo, msgFields), 400

class InstituicaoId(Resource):
    def get(self, id):
            instituicao = InstituicaoEnsino.query.get(uuid.UUID(id))

            if instituicao is None:
                logger.error(f"Instituicao de Ensino de id: {id} não encontrada")

                codigo = Message(1, f"Instituicao de Ensino de id: {id} não encontrada")
                return marshal(codigo, msgFields), 404

            logger.info(f"Instituicao de Ensino de id: {id} listada com sucesso!")
            return marshal(instituicao, instituicaoEnsinoFields), 200

    def put(self, id):
        try:
            args = parser.parse_args()

            instituicao = InstituicaoEnsino.query.get(uuid.UUID(id))

            if instituicao is None:
                logger.error(f"Instituicao de Ensino de id: {id} não encontrada")

                codigo = Message(1, f"Instituicao de Ensino de id: {id} não encontrada")
                return marshal(codigo, msgFields), 404

            instituicao.nome = args['nome']
            instituicao.nome = args['cnpj']

            db.session.add(instituicao)
            db.session.commit()

            logger.info(f"Instituicao de Ensino de id: {id} atualizada com sucesso!")
            return marshal(instituicao, instituicaoEnsinoFields), 200

        except:
          logger.error("Error ao atualizar a Instituicao de Ensino")

          codigo = Message(2, "Error ao atualizar a Instituicao de Ensino")
          return marshal(codigo, msgFields), 400

    def delete(self, id):

        instituicao = InstituicaoEnsino.query.get(uuid.UUID(id))

        if instituicao is None:
            logger.error(f"Instituicao de id: {id} não encontrado")

            codigo = Message(1, f"Instituicao de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404

        db.session.delete(instituicao)
        db.session.commit()

        logger.info(f"Instituicao de id: {id} deletedo com sucesso")
        return []
