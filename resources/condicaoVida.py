from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.condicaoVida import CondicaoVida, condicaoVidaFields
from model.problemaEnfrentado import ProblemaEnfrentados, problemasEnfrentadosFields
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("trabalhoDaFamilia", type=str, help="trabalhoDaFamilia não informado", required=True)
parser.add_argument("quantasPessoasTrabalhamNaCasa", type=int, help="quantasPessoasTrabalhamNaCasa não informado", required=True)
parser.add_argument("rendaMensalFamilia", type=str, help="rendaMensalFamilia não informado", required=True)
parser.add_argument("programaGoverno", type=str, help="programaGoverno não informado", required=True)
parser.add_argument("problemaEnfrentado", type=dict, help="problemaEnfrentado não informado", required=True)

class CondicaoVidas(Resource):
    def get(self):
        condicaoVida = CondicaoVida.query.all()

        logger.info("condicaoVida listadas com sucesso!")
        return marshal(condicaoVida, condicaoVidaFields), 200

class CondicaoVidaId(Resource):
    def put(self, id):
        args = parser.parse_args()
        condicaoVida = CondicaoVida.query.get(uuid.UUID(id))

        if condicaoVida is None:
            logger.error(f"condicaoVida de id: {id} não encontrada")

            codigo = Message(1, f"condicaoVida de id: {id} não encontrada")
            return marshal(codigo, msgFields), 404

        problemaEnfrentado = ProblemaEnfrentados.query.get(condicaoVida.problemaEnfrentado.id)

        problemaEnfrentado.alcool = args['problemaEnfrentado']['alcool']
        problemaEnfrentado.lazer = args['problemaEnfrentado']['lazer']
        problemaEnfrentado.saude = args['problemaEnfrentado']['saude']
        problemaEnfrentado.fome = args['problemaEnfrentado']['fome']
        problemaEnfrentado.drogas = args['problemaEnfrentado']['drogas']
        problemaEnfrentado.violencia = args['problemaEnfrentado']['violencia']
        problemaEnfrentado.desemprego = args['problemaEnfrentado']['desemprego']

        db.session.add(problemaEnfrentado)

        condicaoVida.trabalhoDaFamilia = args['trabalhoDaFamilia']
        condicaoVida.quantasPessoasTrabalhamNaCasa = args['quantasPessoasTrabalhamNaCasa']
        condicaoVida.rendaMensalFamilia = args['rendaMensalFamilia']
        condicaoVida.programaGoverno = args['programaGoverno']
        condicaoVida.problemaEnfrentado = problemaEnfrentado

        db.session.add(condicaoVida)
        db.session.commit()

        return marshal(condicaoVida, condicaoVidaFields), 200

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