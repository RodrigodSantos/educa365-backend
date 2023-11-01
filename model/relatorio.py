from flask_restful import fields
from helpers.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

from model.educando import educandoFields
from model.funcionario import funcionarioFields
from utils.dateFormat import DateFormat

relatorioFields = {
    'id': fields.String,
    'tipo': fields.String,
    'titulo': fields.String,
    'dataCriacao': DateFormat,
    'educando': fields.Nested(educandoFields),
    'funcionario': fields.Nested(funcionarioFields)
}

class Relatorio(db.Model):
    __tablename__= 'tb_relatorio'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    educando_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_educando.pessoa_id"), nullable=False)
    funcionario_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_funcionario.pessoa_id"), nullable=False)

    relatorio = db.Column(db.LargeBinary, nullable=False)
    tipo = db.Column(db.String, nullable=False)
    titulo = db.Column(db.String, nullable=False)
    dataCriacao = db.Column(db.DateTime, default=datetime.datetime.now)

    educando = db.relationship("Educando", uselist=False)
    funcionario = db.relationship("Funcionario", uselist=False)

    def __init__(self, relatorio, tipo, titulo, educando, funcionario):
        self.relatorio = relatorio
        self.tipo = tipo
        self.titulo = titulo
        self.educando = educando
        self.funcionario = funcionario

    def __repr__(self):
        return f'<Turma {self.nome}>'