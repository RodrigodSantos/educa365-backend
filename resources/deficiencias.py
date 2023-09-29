from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.deficiencia import Deficiencia, deficienciaFields
from model.mensagem import Message, msgFields

class Deficiencias(Resource):
    def get(self):
        deficiencia = Deficiencia.query.all()

        logger.info("Deficiencias listadas com sucesso!")
        return marshal(deficiencia, deficienciaFields), 200

class DeficienciaId(Resource):
    def delete(self, id):

        deficiencia = Deficiencia.query.get(uuid.UUID(id))

        if deficiencia is None:
            logger.error(f"Deficiencia de id: {id} não encontrada")

            codigo = Message(1, f"Deficiencia de id: {id} não encontrada")
            return marshal(codigo, msgFields), 404

        db.session.delete(deficiencia)
        db.session.commit()

        logger.info(f"Turma de id: {id} deletedo com sucesso")
        return []