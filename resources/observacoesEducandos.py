from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.observacoesEducando import ObservacoesEducando, observacoesEducandoFields
from model.mensagem import Message, msgFields

class ObservacoesEducandos(Resource):
    def get(self):
        observacoes = ObservacoesEducando.query.all()

        logger.info("Observacoes listadas com sucesso!")
        return marshal(observacoes, observacoesEducandoFields), 200

class ObservacoesEducandoId(Resource):
    def delete(self, id):

        observacoes = ObservacoesEducando.query.get(uuid.UUID(id))

        if observacoes is None:
            logger.error(f"Observacao de id: {id} não encontrada")

            codigo = Message(1, f"Observacao de id: {id} não encontrada")
            return marshal(codigo, msgFields), 404

        db.session.delete(observacoes)
        db.session.commit()

        logger.info(f"Turma de id: {id} deletedo com sucesso")
        return []