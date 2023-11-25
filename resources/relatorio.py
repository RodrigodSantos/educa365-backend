from flask import request, send_file
from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger
from helpers.auth.token_verifier import token_verify

import io
import uuid

from model.funcionario import Funcionario
from model.relatorio import Relatorio, relatorioFields, relatorioTokenFields
from model.educando import Educando
from utils.mensagem import Message, msgFields

class Relatorios(Resource):
  @token_verify
  def get(self, cargo, next_token, token_id):
    if cargo not in ["COORDENADOR(A)", "ASSISTENTE_SOCIAL", "PROFESSOR(A)"]:
        logger.error(f"Funcionario não autorizado!")

        codigo = Message(1, f"Funcionario não autorizado!")
        return marshal(codigo, msgFields), 404

    relatorios = Relatorio.query.all()

    data = {"relatorio": relatorios, "token": next_token}

    logger.info("Relatorios listados com sucesso!")
    return marshal(data, relatorioTokenFields), 200

  @token_verify
  def post(self, cargo, next_token, token_id):
    if cargo not in ["COORDENADOR(A)", "ASSISTENTE_SOCIAL", "PROFESSOR(A)"]:
        logger.error(f"Funcionario não autorizado!")

        codigo = Message(1, f"Funcionario não autorizado!")
        return marshal(codigo, msgFields), 404

    arquivo = request.files["relatorio"].read()
    titulo = request.form.get("titulo")
    educando_id = request.form.get("educando_id", None)
    funcionario_id = request.form.get("funcionario_id")

    educando = None
    if educando_id:
      educando = Educando.query.get(educando_id)

    funcionario = Funcionario.query.get(funcionario_id)

    if funcionario is None:
      logger.error(f"Funcionario de id: {funcionario_id} não encontrado")

      codigo = Message(1, f"Funcionario de id: {funcionario_id} não encontrado")
      return marshal(codigo, msgFields), 404

    relatorio = Relatorio(
      arquivo,
      titulo,
      educando,
      funcionario
    )

    db.session.add(relatorio)
    db.session.commit()

    data = {"relatorio": relatorio, "token": next_token}

    logger.info(f"Relatorio de id: {relatorio.id} criado com sucesso")
    return marshal(data, relatorioTokenFields), 200

class RelatorioId(Resource):

  @token_verify
  def get(self, cargo, next_token, token_id, id):
    if cargo not in ["COORDENADOR(A)", "ASSISTENTE_SOCIAL", "PROFESSOR(A)"]:
        logger.error(f"Funcionario não autorizado!")

        codigo = Message(1, f"Funcionario não autorizado!")
        return marshal(codigo, msgFields), 404

    relatorio = Relatorio.query.get(uuid.UUID(id))

    if relatorio is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    binary_data = relatorio.relatorio

    response = send_file(io.BytesIO(binary_data), mimetype='application/pdf', as_attachment=False, download_name='output.pdf')

    logger.info(f"Relatorio de id: {id} listado com sucesso!")
    return response

  @token_verify
  def put(self, cargo, next_token, token_id, id):
    if cargo not in ["COORDENADOR(A)", "ASSISTENTE_SOCIAL", "PROFESSOR(A)"]:
        logger.error(f"Funcionario não autorizado!")

        codigo = Message(1, f"Funcionario não autorizado!")
        return marshal(codigo, msgFields), 404

    relatorio = request.files["relatorio"].read()
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
    relatorioBd.titulo = titulo
    relatorioBd.funcionario = funcionario

    if educando != None:
      relatorioBd.educando = educando

    db.session.add(relatorioBd)
    db.session.commit()

    data = {"relatorio": relatorioBd, "token": next_token}

    logger.info(f"Relatorio de id: {id} atualizado com sucesso!")
    return marshal(data, relatorioTokenFields), 200

  @token_verify
  def delete(self, cargo, next_token, token_id, id):
    if cargo not in ["COORDENADOR(A)", "ASSISTENTE_SOCIAL", "PROFESSOR(A)"]:
        logger.error(f"Funcionario não autorizado!")

        codigo = Message(1, f"Funcionario não autorizado!")
        return marshal(codigo, msgFields), 404
    relatorio = Relatorio.query.get(uuid.UUID(id))

    if relatorio is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(relatorio)
    db.session.commit()

    data = {"token": next_token}

    return data

class RelatorioDadosId(Resource):

  @token_verify
  def get(self, cargo, next_token, token_id, id):
    if cargo not in ["COORDENADOR(A)", "ASSISTENTE_SOCIAL", "PROFESSOR(A)"]:
        logger.error(f"Funcionario não autorizado!")

        codigo = Message(1, f"Funcionario não autorizado!")
        return marshal(codigo, msgFields), 404
    relatorio = Relatorio.query.get(uuid.UUID(id))

    if relatorio is None:
      logger.error(f"Relatorio de id: {id} não encontrado")

      codigo = Message(1, f"Relatorio de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    data = {"relatorio": relatorio, "token": next_token}

    logger.info(f"Dados do Relatorio de id: {id} listados com sucesso!")
    return marshal(data, relatorioTokenFields), 200