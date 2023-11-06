from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.condicaoMoradia import CondicaoMoradia, condicaoMoradiaFields
from utils.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("tipoCasa", type=str, help="tipoCasa não informado", required=True)
parser.add_argument("posseCasa", type=str, help="posseCasa não informado", required=True)
parser.add_argument("banheiroComFossa", type=bool, help="banheiroComFossa não informado", required=True)
parser.add_argument("aguaCagepa", type=bool, help="aguaCagepa não informado", required=True)
parser.add_argument("poco", type=bool, help="poco não informado", required=True)
parser.add_argument("energia", type=bool, help="energia não informado", required=True)

class CondicaoMoradias(Resource):
    def get(self):
        condicaoMoradia = CondicaoMoradia.query.all()

        logger.info("condicaoMoradia listadas com sucesso!")
        return marshal(condicaoMoradia, condicaoMoradiaFields), 200

class CondicaoMoradiaId(Resource):
    def put(self, id):
        args = parser.parse_args()
        condicaoMoradia = CondicaoMoradia.query.get(uuid.UUID(id))

        if condicaoMoradia is None:
            logger.error(f"condicaoMoradia de id: {id} não encontrada")

            codigo = Message(1, f"condicaoMoradia de id: {id} não encontrada")
            return marshal(codigo, msgFields), 404

        condicaoMoradia.tipoCasa = args['tipoCasa']
        condicaoMoradia.posseCasa = args['posseCasa']
        condicaoMoradia.banheiroComFossa = args['banheiroComFossa']
        condicaoMoradia.aguaCagepa = args['aguaCagepa']
        condicaoMoradia.poco = args['poco']
        condicaoMoradia.energia = args['energia']

        db.session.add(condicaoMoradia)
        db.session.commit()

        return marshal(condicaoMoradia, condicaoMoradiaFields), 200

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