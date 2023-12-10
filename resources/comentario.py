import io
import uuid
from flask_restful import Resource, marshal, reqparse

from helpers.log import logger
from helpers.database import db
from helpers.auth.token_verifier import token_verify
from utils.mensagem import Message, msgFields
from model.comentario import Comentario, comentarioFields
from model.comentarioRelatorio import ComentarioRelatorio

parser = reqparse.RequestParser()

parser.add_argument("texto", type=str, help="Texto não informado", required=True)
parser.add_argument("relatorio_id", type=str, help="Relatório não informada", required=True)
parser.add_argument("funcionario_id", type=str, help="Funcionário não informada", required=True)

class Comentarios(Resource):
  @token_verify
  def get(self, cargo, next_token, token_id):
    comentarios = Comentario.query.all()

    logger.info("Turmas listadas com sucesso!")
    return marshal(comentarios, comentarioFields), 200

  @token_verify
  def post(self, cargo, next_token, token_id):
    args = parser.parse_args()
    texto = args["texto"]
    relatorio_id = args["relatorio_id"]
    funcionario_id = args["funcionario_id"]

    comentario = Comentario(texto, relatorio_id, funcionario_id)

    db.session.add(comentario)
    db.session.commit()

    comentarioRelatorio = ComentarioRelatorio(comentario.id, relatorio_id)
    db.session.add(comentarioRelatorio)
    db.session.commit()

    logger.info(f"Comentário de id: {comentario.id} criado com sucesso")
    return marshal(comentario, comentarioFields)

class ComentariosId(Resource):
  @token_verify
  def delete(self, cargo, next_token, token_id, id):
    comentario = Comentario.query.get(uuid.UUID(id))

    if comentario is None:
      logger.error(f"Comentário de id: {id} não encontrado")

      codigo = Message(1, f"Comentário de id: {id} não encontrado")
      return marshal(codigo, msgFields), 404

    db.session.delete(comentario)
    db.session.commit()
    logger.info(f"Comentário de id: {id} deletado com sucesso!")
    return ([], 200)
