from flask_restful import fields
from helpers.database import db
from utils.dateFormat import DateFormat

from model.educando import educandoFields
from model.responsavel import responsavelFields
from model.endereco import enderecoFields
from model.turma import turmaFields
from model.instituicaoEnsino import instituicaoEnsinoFields
from model.observacoesEducando import observacoesEducandoFields

import uuid

educandoResponsavelFields = {
  "id": fields.String,
  'nome': fields.String,
  'sexo': fields.Boolean,
  'dataNascimento': DateFormat,
  'rg': fields.String,
  'cpf': fields.String,
  "nis": fields.String,
  "cidadeCartorio": fields.String,
  "sus": fields.String,
  "nomeCartorio": fields.String,
  "numeroRegistroNascimento": fields.String,
  "dataEmissaoCertidao": DateFormat,
  "ufCartorio": fields.String,
  "etnia": fields.String,
  "nomeMae": fields.String,
  "nomePai": fields.String,
  "dataMatricula": DateFormat,
  "endereco": fields.Nested(enderecoFields),
  "turma": fields.Nested(turmaFields),
  "observacoesEducando": fields.Nested(observacoesEducandoFields),
  "responsaveis": fields.Nested(responsavelFields)
}

educandoResponsaveisFields = {
    "id": fields.String,
    "educando": fields.Nested(educandoFields),
    "responsavel": fields.Nested(responsavelFields)
}

class EducandoResponsavel(db.Model):
    __tablename__ = "tb_educando_responsavel"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    educando_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_educando.pessoa_id"))
    responsavel_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_responsavel.pessoa_id"))

    educando = db.relationship("Educando", uselist=False, backref=db.backref("tb_educando"))
    responsavel = db.relationship("Responsavel", uselist=False, backref=db.backref("tb_responsavel"))

    def __init__(self, educando, responsavel):
        self.educando = educando
        self.responsavel = responsavel

    def __repr__(self):
        return self