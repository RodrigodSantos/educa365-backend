from flask_restful import fields
from helpers.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

instituicaoEnsinoFields = {
    "id": fields.String,
    "nome": fields.String,
    "cnpj": fields.String
}

class InstituicaoEnsino(db.Model):
    __tablename__ = 'tb_instituicao_ensino'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String, nullable=False)
    cnpj = db.Column(db.String, nullable=False)

    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj

    def __repr__(self):
        return f'<InstituicaoEnsino {self.nome}>'