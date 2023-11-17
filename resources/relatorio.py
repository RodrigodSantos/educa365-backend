from flask import request, send_file
from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger
import io
import uuid
from model.funcionario import Funcionario

from model.relatorio import Relatorio, relatorioFields
from model.educando import Educando
from utils.mensagem import Message, msgFields

class Relatorios(Resource):
  def get(self):
    relatorios = Relatorio.query.all()

    logger.info("Relatorios listados com sucesso!")
    return marshal(relatorios, relatorioFields), 200

  def post(self):
    arquivo = request.files["relatorio"].read()
    tipo = request.form.get("tipo")
    titulo = request.form.get("titulo")
    educando_id = request.form.get("educando_id", None)
    funcionario_id = request.form.get("funcionario_id")

    educando = None
    if educando_id:
      educando = Educando.query.get(educando_id)

    funcionario = Funcionario.query.get(funcionario_id)

    if funcionario is None:
      logger.error(f"Funcionario de id: {id} não encontrado")

      codigo = Message(1, f"Funcionario de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    relatorio = Relatorio(
      arquivo,
      tipo,
      titulo,
      educando,
      funcionario
    )

    db.session.add(relatorio)
    db.session.commit()

    logger.info(f"Relatorio de id: {relatorio.id} criado com sucesso")
    return marshal(relatorio, relatorioFields), 200

class RelatorioId(Resource):
  def get(self, id):
    relatorio = Relatorio.query.get(uuid.UUID(id))

    if relatorio is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    binary_data = relatorio.relatorio

    response = send_file(io.BytesIO(binary_data), mimetype='application/pdf', as_attachment=False, download_name='output.pdf')

    logger.info(f"Relatorio de id: {id} listado com sucesso!")
    return response

  def put(self, id):
    relatorio = request.files["relatorio"].read()
    tipo = request.form.get("tipo")
    titulo = request.form.get("titulo")
    educando_id = request.form.get("educando_id", None)
    funcionario_id = request.form.get("funcionario_id")

    educando = None
    if educando_id:
      educando = Educando.query.get(educando_id)

    funcionario = Funcionario.query.get(funcionario_id)

    if funcionario is None:
      logger.error(f"Funcionario de id: {id} não encontrado")

      codigo = Message(1, f"Funcionario de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    relatorioBd = Relatorio.query.get(uuid.UUID(id))

    if relatorioBd is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    relatorioBd.relatorio = relatorio
    relatorioBd.tipo = tipo
    relatorioBd.titulo = titulo
    relatorioBd.funcionario = funcionario

    if educando != None:
      relatorioBd.educando = educando

    db.session.add(relatorioBd)
    db.session.commit()

    logger.info(f"Relatorio de id: {id} atualizado com sucesso!")
    return f"Relatorio de id: {id} atualizado com sucesso!"

  def delete(self, id):
    relatorio = Relatorio.query.get(uuid.UUID(id))

    if relatorio is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(relatorio)
    db.session.commit()

    return []

class RelatorioDadosId(Resource):
  def get(self, id):
    relatorioAcademico = Relatorio.query.get(uuid.UUID(id))

    if relatorioAcademico is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    logger.info(f"Dados do Relatorio de id: {id} listados com sucesso!")
    return marshal(relatorioAcademico, relatorioFields), 200