from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.turma import Turma, turmaFields
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)

class Turmas(Resource):
    def get(self):
        turma = Turma.query.all()

        logger.info("Turmas listadas com sucesso!")
        return marshal(turma, turmaFields), 200

    def post(self):
        try:
            args = parser.parse_args()

            turma = Turma(
                args['nome']
            )

            db.session.add(turma)
            db.session.commit()

            logger.info(f"Turma de id: {turma.id} criado com sucesso")
            return marshal(turma, turmaFields)

        except:
            logger.error("Erro ao cadastrar a Turma")

            codigo = Message(2, "Erro ao cadastrar a Turma")
            return marshal(codigo, msgFields), 400

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