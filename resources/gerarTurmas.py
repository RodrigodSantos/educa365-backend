from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.turma import Turma, turmaFields
from model.instituicaoEnsino import InstituicaoEnsino, instituicaoEnsinoFields
from utils.mensagem import Message, msgFields

class GerarTurmas(Resource):
  def post(self):

    turmas = Turma.query.all()

    instituicao_1 = InstituicaoEnsino("Creche","11.111.111/1111-11")
    db.session.add(instituicao_1)

    lista = []
    for turma in turmas:
      lista.append(
        {
          "nome": turma.nome,
          "turno": turma.turno
        }
      )
    if {"nome": "Pré-1", "turno": "Manhã"} not in lista:
      db.session.add(Turma("Pré-1", "Manhã", instituicao_1))
    if {"nome": "Pré-1", "turno": "Tarde"} not in lista:
      db.session.add(Turma("Pré-1", "Tarde", instituicao_1))
    if {"nome": "Pré-2", "turno": "Manhã"} not in lista:
      db.session.add(Turma("Pré-2", "Manhã", instituicao_1))
    if {"nome": "Pré-2", "turno": "Tarde"} not in lista:
      db.session.add(Turma("Pré-2", "Tarde", instituicao_1))
    if {"nome": "Maternal-C", "turno": "Integral"} not in lista:
      db.session.add(Turma("Maternal-C", "Integral", instituicao_1))

    db.session.commit()