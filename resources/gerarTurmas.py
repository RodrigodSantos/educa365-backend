from flask_restful import Resource
from helpers.database import db

from model.turma import Turma
from model.instituicaoEnsino import InstituicaoEnsino

class GerarTurmas(Resource):
  def post(self):

    turmas = Turma.query.all()

    instituicao_1 = InstituicaoEnsino("Creche","11.111.111/1111-11")
    instituicao_2 = InstituicaoEnsino("Escola","22.222.222/2222-22")
    db.session.add(instituicao_1)
    db.session.add(instituicao_2)

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
    if {"nome": "Turma-a", "turno": "Manhã"} not in lista:
      db.session.add(Turma("Turma-a", "Manhã", instituicao_2))
    if {"nome": "Turma-a", "turno": "Tarde"} not in lista:
      db.session.add(Turma("Turma-a", "Tarde", instituicao_2))
    if {"nome": "Turma-b", "turno": "Manhã"} not in lista:
      db.session.add(Turma("Turma-b", "Manhã", instituicao_2))
    if {"nome": "Turma-b", "turno": "Tarde"} not in lista:
      db.session.add(Turma("Turma-b", "Tarde", instituicao_2))

    db.session.commit()

  def delete(self):
    db.session.query(Turma).delete()
    db.session.commit()
    return []
