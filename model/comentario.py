import uuid
import datetime
from flask_restful import fields
from helpers.database import db
from sqlalchemy.dialects.postgresql import UUID

from utils.dateFormat import DateTimeFormat
from model.funcionario import funcionarioFields

comentarioFields = {
    "id": fields.String,
    "texto": fields.String,
    "dataCriacao": DateTimeFormat,
    "funcionario": fields.Nested(funcionarioFields),
    # "relatorio": fields.Nested(relatorioFields),
}

class Comentario(db.Model):
    __tablename__ = "tb_comentario"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    relatorio_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_relatorio.id"), nullable=False)
    funcionario_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_funcionario.pessoa_id"), nullable=False)

    texto = db.Column(db.String, nullable=False)
    dataCriacao = db.Column(db.DateTime, default=datetime.datetime.now)

    funcionario = db.relationship("Funcionario", uselist=False)

    def __init__(self, texto, relatorio_id, funcionario_id):
        self.texto = texto
        self.relatorio_id = relatorio_id
        self.funcionario_id = funcionario_id

    def __repr__(self):
        return self