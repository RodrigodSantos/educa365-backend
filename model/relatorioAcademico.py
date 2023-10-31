from flask_restful import fields
from helpers.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

from model.educando import educandoFields
from utils.dateFormat import DateFormat

relatorioAcademicoFields = {
    'id': fields.String,
    'educando': fields.Nested(educandoFields),
    'dataEnvio': DateFormat
}

class RelatorioAcademico(db.Model):
    __tablename__= 'tb_relatorio_academico'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    educando_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_educando.pessoa_id"), nullable=False)

    relatorio = db.Column(db.LargeBinary, nullable=False)
    dataEnvio = db.Column(db.DateTime, default=datetime.datetime.now)

    educando = db.relationship("Educando", uselist=False)

    def __init__(self, educando, relatorio):
        self.educando = educando
        self.relatorio = relatorio

    def __repr__(self):
        return f'<Turma {self.nome}>'