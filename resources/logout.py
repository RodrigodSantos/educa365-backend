from flask_restful import Resource, marshal, reqparse, request
from model.blackList import BlackList
from helpers.database import db
from utils.mensagem import Message, msgFields
from jwt import decode
from datetime import datetime
from helpers.auth.token_verifier import token_verify

class Logout(Resource):

  @token_verify
  def post(self, cargo, token, token_id):
    try:
      rawToken = request.headers["Authorization"]
      token = rawToken.split()[1]

      informationToken = decode(token, key="1234", algorithms="HS256")
      tokenExp = informationToken['exp']
      blackToken = BlackList(token, datetime.fromtimestamp(tokenExp))

      db.session.add(blackToken)
      db.session.commit()

      codigo = Message(0, "Logout Realizado com sucesso")
      return marshal(codigo, msgFields), 200

    except IndexError:
      codigo = Message(1, "Schema de autenticação nao informado")
      return marshal(codigo, msgFields), 400

    except:
      codigo = Message(2, "Erro ao fazer logout")
      return marshal(codigo, msgFields), 400