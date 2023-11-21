from functools import wraps

from flask_restful import request, marshal

from jwt import decode, InvalidSignatureError, ExpiredSignatureError

from model.blackList import BlackList
from .token_handler import token_creator

from helpers.log import logger

from utils.mensagem import Message, msgFields
from utils.token import Token, tokenFields

def token_verify(function: callable) -> callable:

  @wraps(function)
  def decorated(*args, **kwargs):
    rawToken = request.headers["Authorization"]
    if not rawToken:
      logger.error("Sem token!")

      codigo = Message(1, "Sem token!")
      return marshal(codigo, msgFields), 401

    try:
      token = rawToken.split()[1]
      informationToken = decode(token, key="1234", algorithms="HS256")
      cargo = informationToken['cargo']
      token_id = informationToken['id']

    except InvalidSignatureError:
      token = Token("Token invalido")
      return marshal(token, tokenFields), 401

    except ExpiredSignatureError:
      token = Token("Token Expirado")
      return marshal(token, tokenFields), 401

    except KeyError:
      token = Token("Token com campos faltando")
      return marshal(token, tokenFields), 401

    except IndexError:
      codigo = Message(1, "Schema de autenticação nao informado")
      return marshal(codigo, msgFields), 400

    blackToken = BlackList.query.filter_by(token=token).first()

    if blackToken:
      token = Token("Token na black list")
      return marshal(token, tokenFields), 401

    next_token = token_creator.refresh(token)
    return function(*args, cargo, next_token, token_id, **kwargs)

  return decorated