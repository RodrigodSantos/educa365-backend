from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.instituicaoEnsino import InstituicaoEnsino, instituicaoEnsinoFields
from model.mensagem import Message, msgFields

class Instituicoes(Resource):
    def get(self):
        instituicao = InstituicaoEnsino.query.all()

        logger.info("Instituicoes listados com sucesso!")
        return marshal(instituicao, instituicaoEnsinoFields), 200

class InstituicaoId(Resource):
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
