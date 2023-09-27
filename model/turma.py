from flask_restful import fields
from helpers.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

turmaFields = {
  "id": fields.String,
  "nome": fields.String
}

class Turma(db.Model):
    __tablename__= 'tb_turma'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String, nullable=False)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f'<Turma {self.nome}>'