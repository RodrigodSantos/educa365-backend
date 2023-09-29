from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.turma import Turma, turmaFields
from model.mensagem import Message, msgFields

class Turmas(Resource):
    def get(self):
        turma = Turma.query.all()

        logger.info("Turmas listadas com sucesso!")
        return marshal(turma, turmaFields), 200

class TurmaId(Resource):
    def delete(self, id):

        turma = Turma.query.get(uuid.UUID(id))

        if turma is None:
            logger.error(f"Turma de id: {id} não encontrada")

            codigo = Message(1, f"Turma de id: {id} não encontrada")
            return marshal(codigo, msgFields), 404

        db.session.delete(turma)
        db.session.commit()

        logger.info(f"Turma de id: {id} deletedo com sucesso")
        return []