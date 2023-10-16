from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.observacoesEducando import ObservacoesEducando, observacoesEducandoFields
from model.deficiencia import Deficiencia
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("alimentacao", type=str, help="alimentacao não informado", required=True)
parser.add_argument("medicacao", type=str, help="medicacao não informado", required=True)
parser.add_argument("produtoHigienePessoal", type=str, help="produtoHigienePessoal não informado", required=True)
parser.add_argument("tipoSangue", type=str, help="tipoSangue não informado", required=True)
parser.add_argument("medicacaoDeficiencia", type=str, help="medicacaoDeficiencia não informado", required=True)
parser.add_argument("laudoMedico", type=bool, help="laudoMedico não informado", required=True)
parser.add_argument("deficiencia", type=dict, help="deficiencia não informado", required=True)

class ObservacoesEducandos(Resource):
    def get(self):
        observacoes = ObservacoesEducando.query.all()

        logger.info("Observacoes listadas com sucesso!")
        return marshal(observacoes, observacoesEducandoFields), 200

class ObservacoesEducandoId(Resource):
    def put(self, id):
        args = parser.parse_args()

        observacoes = ObservacoesEducando.query.get(uuid.UUID(id))

        if observacoes is None:
            logger.error(f"Observacao de id: {id} não encontrada")

            codigo = Message(1, f"Observacao de id: {id} não encontrada")
            return marshal(codigo, msgFields), 404

        deficiencia = Deficiencia.query.get(observacoes.deficiencia.id)

        deficiencia.intelectual = args['deficiencia']['intelectual']
        deficiencia.auditiva = args['deficiencia']['auditiva']
        deficiencia.visual = args['deficiencia']['visual']
        deficiencia.fisica = args['deficiencia']['fisica']
        deficiencia.multipla = args['deficiencia']['multipla']

        db.session.add(deficiencia)

        observacoes.alimentacao = args['alimentacao']
        observacoes.medicacao = args['medicacao']
        observacoes.produtoHigienePessoal = args['produtoHigienePessoal']
        observacoes.tipoSangue = args['tipoSangue']
        observacoes.medicacaoDeficiencia = args['medicacaoDeficiencia']
        observacoes.laudoMedico = args['laudoMedico']
        observacoes.deficiencia = deficiencia

        db.session.add(observacoes)
        db.session.commit()

        return marshal(observacoes, observacoesEducandoFields), 200

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