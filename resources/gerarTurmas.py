from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.turma import Turma, turmaFields
from model.instituicaoEnsino import InstituicaoEnsino, instituicaoEnsinoFields
from utils.mensagem import Message, msgFields

class GerarTurmas(Resource):
  def post(self):
    instituicao_1 = InstituicaoEnsino("Creche","11.111.111/1111-11")

    db.session.add(instituicao_1)

    turma_1 = Turma("Pré-1", "Manhã", instituicao_1)
    turma_2 = Turma("Pré-1", "Tarde", instituicao_1)
    turma_3 = Turma("Pré-2", "Manhã", instituicao_1)
    turma_4 = Turma("Pré-2", "Tarde", instituicao_1)
    turma_5 = Turma("Maternal-C", "Integral", instituicao_1)

    db.session.add(turma_1)
    db.session.add(turma_2)
    db.session.add(turma_3)
    db.session.add(turma_4)
    db.session.add(turma_5)

    db.session.commit()