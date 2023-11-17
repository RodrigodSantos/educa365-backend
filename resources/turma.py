from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid
from model.funcionario import Funcionario

from model.turma import Turma, turmaFields
from model.instituicaoEnsino import InstituicaoEnsino
from utils.mensagem import Message, msgFields

parser = reqparse.RequestParser()
patch_parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("turno", type=str, help="Turno não informado", required=True)
parser.add_argument("instituicao_id", type=str, help="Instituição não informada", required=True)
patch_parser.add_argument("professor_id", type=str, required=True)

class Turmas(Resource):
    def get(self):
        turma = Turma.query.all()

        logger.info("Turmas listadas com sucesso!")
        return marshal(turma, turmaFields), 200

    def post(self):
        try:
            args = parser.parse_args()

            instituicao = InstituicaoEnsino.query.get(args['instituicao_id'])

            if instituicao is None:
                logger.error(f"Instituição de id: {args['instituicao_id']} não encontrado")

                codigo = Message(1, f"Instituição de id: {args['instituicao_id']} não encontrado")
                return marshal(codigo, msgFields), 404

            turma = Turma(
                args['nome'],
                args['turno'],
                instituicao
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
    def get(self, id):
            turma = Turma.query.get(uuid.UUID(id))

            if turma is None:
                logger.error(f"Turma de id: {id} não encontrada")

                codigo = Message(1, f"Turma de id: {id} não encontrada")
                return marshal(codigo, msgFields), 404

            logger.info(f"Turma de id: {id} listada com sucesso!")
            return marshal(turma, turmaFields), 200

    def put(self, id):
        try:
            args = parser.parse_args()

            turma = Turma.query.get(uuid.UUID(id))
            instituicao = InstituicaoEnsino.query.get(args['instituicao_id'])


            if turma is None:
                logger.error(f"Turma de id: {id} não encontrada")

                codigo = Message(1, f"Turma de id: {id} não encontrada")
                return marshal(codigo, msgFields), 404

            if instituicao is None:
                logger.error(f"Instituição de id: {args['instituicao_id']} não encontrado")

                codigo = Message(1, f"Instituição de id: {args['instituicao_id']} não encontrado")
                return marshal(codigo, msgFields), 404

            turma.nome = args['nome']
            turma.turno = args['turno']
            turma.instituicao = instituicao

            db.session.add(turma)
            db.session.commit()

            logger.info(f"Turma de id: {id} atualizada com sucesso!")
            return marshal(turma, turmaFields), 200

        except:
          logger.error("Error ao atualizar a Turma")

          codigo = Message(2, "Error ao atualizar a Turma")
          return marshal(codigo, msgFields), 400

    def patch(self, id):
        try:
            args = patch_parser.parse_args()
            turma = Turma.query.get(uuid.UUID(id))
            professor = Funcionario.query.get(args['professor_id'])

            if turma is None:
                logger.error(f"Turma de id: {id} não encontrada")

                codigo = Message(1, f"Turma de id: {id} não encontrada")
                return marshal(codigo, msgFields), 404

            if professor is None:
                logger.error(f"Professor de id: {id} não encontrada")

                codigo = Message(1, f"Professor de id: {id} não encontrada")
                return marshal(codigo, msgFields), 404

            turma.professor = professor

            db.session.add(turma)
            db.session.commit()

            logger.info(f"Turma de id: {id} atualizada com sucesso!")
            return marshal(turma, turmaFields), 200

        except:
            logger.error(f"Erro ao atualizar a Turma")

            codigo = Message(2, "Erro ao atualizar a Turma")
            return marshal(codigo, msgFields), 400

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
