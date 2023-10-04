from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.condicaoMoradia import CondicaoMoradia, condicaoMoradiaFields
from model.mensagem import Message, msgFields

class CondicaoMoradias(Resource):
    def get(self):
        condicaoMoradia = CondicaoMoradia.query.all()

        logger.info("condicaoMoradia listadas com sucesso!")
        return marshal(condicaoMoradia, condicaoMoradiaFields), 200

class CondicaoMoradiaId(Resource):
    def delete(self, id):

        condicaoMoradia = CondicaoMoradia.query.get(uuid.UUID(id))

        if condicaoMoradia is None:
            logger.error(f"condicaoMoradia de id: {id} não encontrada")

            codigo = Message(1, f"condicaoMoradia de id: {id} não encontrada")
            return marshal(codigo, msgFields), 404

        db.session.delete(condicaoMoradia)
        db.session.commit()

        logger.info(f"condicaoMoradia de id: {id} deletedo com sucesso")
        return []