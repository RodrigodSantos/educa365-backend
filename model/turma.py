from flask_restful import fields
from helpers.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

from model.instituicaoEnsino import instituicaoEnsinoFields
from model.funcionario import funcionarioFields

turmaFields = {
  "id": fields.String,
  "nome": fields.String,
  "turno": fields.String,
  "instituicao": fields.Nested(instituicaoEnsinoFields),
  "professor": fields.Nested(funcionarioFields)
}

class Turma(db.Model):
    __tablename__= 'tb_turma'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instituicao_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_instituicao_ensino.id"), nullable=False)
    professor_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_funcionario.pessoa_id"), nullable=True)
    nome = db.Column(db.String, nullable=False)
    turno = db.Column(db.String, nullable=False)

    instituicao = db.relationship("InstituicaoEnsino", uselist=False)
    professor = db.relationship("Funcionario", uselist=False)

    def __init__(self, nome, turno, instituicao):
        self.nome = nome
        self.turno = turno
        self.instituicao = instituicao

    def __repr__(self):
        return f'<Turma {self.nome}>'