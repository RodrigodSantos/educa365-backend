from flask_restful import Resource
from helpers.database import db
from model.educandoResponsavel import EducandoResponsavel

from utils.calculoIdade import calcular_idade

from model.turma import Turma
from model.instituicaoEnsino import InstituicaoEnsino
from model.educando import Educando

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

    turma_1 = Turma("Pré-1", "Manhã", instituicao_1)
    turma_2 = Turma("Pré-1", "Tarde", instituicao_1)
    turma_3 = Turma("Pré-2", "Manhã", instituicao_1)
    turma_4 = Turma("Pré-2", "Tarde", instituicao_1)
    turma_5 = Turma("Maternal-C", "Integral", instituicao_1)
    turma_6 = Turma("Turma-a", "Manhã", instituicao_2)
    turma_7 = Turma("Turma-a", "Tarde", instituicao_2)
    turma_8 = Turma("Turma-b", "Manhã", instituicao_2)
    turma_9 = Turma("Turma-b", "Tarde", instituicao_2)

    if {"nome": "Pré-1", "turno": "Manhã"} not in lista:
      db.session.add(turma_1)
    if {"nome": "Pré-1", "turno": "Tarde"} not in lista:
      db.session.add(turma_2)
    if {"nome": "Pré-2", "turno": "Manhã"} not in lista:
      db.session.add(turma_3)
    if {"nome": "Pré-2", "turno": "Tarde"} not in lista:
      db.session.add(turma_4)
    if {"nome": "Maternal-C", "turno": "Integral"} not in lista:
      db.session.add(turma_5)
    if {"nome": "Turma-a", "turno": "Manhã"} not in lista:
      db.session.add(turma_6)
    if {"nome": "Turma-a", "turno": "Tarde"} not in lista:
      db.session.add(turma_7)
    if {"nome": "Turma-b", "turno": "Manhã"} not in lista:
      db.session.add(turma_8)
    if {"nome": "Turma-b", "turno": "Tarde"} not in lista:
      db.session.add(turma_9)

    educandos = Educando.query.all()

    for x, educando in enumerate(educandos):
      # if educando.turma is not None:
      #   break
      idade = calcular_idade(educando.dataNascimento)

      if idade == 3:
        educando.turma = turma_5

      elif idade == 4 and (x % 2) == 0:
        educando.turma = turma_1
      elif idade == 4 and (x % 2) > 0:
        educando.turma = turma_2

      elif idade == 5 and (x % 2) == 0:
        educando.turma = turma_3
      elif idade == 5 and (x % 2) > 0:
        educando.turma = turma_4

      elif idade >= 6 and idade <= 11 and (x % 2) == 0:
        educando.turma = turma_6
      elif idade >= 6 and idade <= 11 and (x % 2) > 0:
        educando.turma = turma_7

      elif idade >= 6 and idade <= 11 and (x % 2) == 0:
        educando.turma = turma_8
      elif idade >= 6 and idade <= 11 and (x % 2) > 0:
        educando.turma = turma_9

      db.session.add(educando)

    db.session.commit()

  def delete(self):
    db.session.query(EducandoResponsavel).delete()
    db.session.query(Educando).delete()
    db.session.query(Turma).delete()
    db.session.commit()

    return []