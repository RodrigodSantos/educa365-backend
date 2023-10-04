from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.condicaoVida import CondicaoVida, condicaoVidaFields
from model.mensagem import Message, msgFields

class CondicaoVidas(Resource):
    def get(self):
        condicaoVida = CondicaoVida.query.all()

        logger.info("condicaoVida listadas com sucesso!")
        return marshal(condicaoVida, condicaoVidaFields), 200

class CondicaoVidaId(Resource):
    def delete(self, id):

        condicaoVida = CondicaoVida.query.get(uuid.UUID(id))

        if condicaoVida is None:
            logger.error(f"condicaoVida de id: {id} não encontrada")

            codigo = Message(1, f"condicaoVida de id: {id} não encontrada")
            return marshal(codigo, msgFields), 404

        db.session.delete(condicaoVida)
        db.session.commit()

        logger.info(f"condicaoVida de id: {id} deletedo com sucesso")
        return []