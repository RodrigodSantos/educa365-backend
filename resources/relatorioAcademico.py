from flask import request, send_file
from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger
import io
import uuid

from model.relatorioAcademico import RelatorioAcademico, relatorioAcademicoFields
from model.educando import Educando
from utils.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("educando_id", type=str, help="educando_id não informado", required=False)

class RelatorioAcademicoId(Resource):
  def get(self, id):
    relatorioAcademico = RelatorioAcademico.query.get(uuid.UUID(id))

    if relatorioAcademico is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    binary_data = relatorioAcademico.relatorio

    response = send_file(io.BytesIO(binary_data), mimetype='application/pdf', as_attachment=False, download_name='output.pdf')

    logger.info(f"Relatorio de id: {id} listado com sucesso!")
    return response

  def post(self, id):
    educando = Educando.query.get(uuid.UUID(id))
    relatorio = request.data

    if educando is None:
      logger.error(f"Educando de id: {id} não encontrado")

      codigo = Message(1, f"Educando de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    relatorioAcademico = RelatorioAcademico(
      educando,
      relatorio
    )

    db.session.add(relatorioAcademico)
    db.session.commit()

    logger.info(f"Relatorio de id: {relatorioAcademico.id} criado com sucesso")
    return f"Relatorio de id: {relatorioAcademico.id} criado com sucesso"

  def put(self, id):
    relatorioAcademico = RelatorioAcademico.query.get(uuid.UUID(id))
    relatorio = request.data

    if relatorioAcademico is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    relatorioAcademico.relatorio = relatorio

    db.session.add(relatorioAcademico)
    db.session.commit()

    logger.info(f"Relatorio de id: {id} atualizado com sucesso!")
    return f"Relatorio de id: {id} atualizado com sucesso!"

  def delete(self, id):
    relatorio = RelatorioAcademico.query.get(uuid.UUID(id))

    if relatorio is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(relatorio)
    db.session.commit()

    return []

class RelatorioAcademicoDadosId(Resource):
  def get(self, id):
    relatorioAcademico = RelatorioAcademico.query.get(uuid.UUID(id))

    if relatorioAcademico is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    logger.info(f"Dados do Relatorio de id: {id} listados com sucesso!")
    return marshal(relatorioAcademico, relatorioAcademicoFields), 200

  def put(self, id):
    args = parser.parse_args()

    relatorioAcademico = RelatorioAcademico.query.get(uuid.UUID(id))
    educando = Educando.query.get(args['educando_id'])

    if educando is None:
      logger.error(f"Educando de id: {id} não encontrado")

      codigo = Message(1, f"Educando de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    if relatorioAcademico is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    relatorioAcademico.educando = educando

    db.session.add(relatorioAcademico)
    db.session.commit()

    logger.info(f"Relatorio de id: {id} atualizado com sucesso!")
    return marshal(relatorioAcademico, relatorioAcademicoFields), 200
