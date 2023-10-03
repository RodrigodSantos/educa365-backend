from flask_restful import fields
from helpers.database import db
from model.problemaEnfrentado import problemasEnfrentadosFields
from sqlalchemy.dialects.postgresql import UUID
import uuid

condicaoVidaFields = {
    "id": fields.String,
    "trabalhoDaFamilia": fields.String,
    "quantasPessoasTrabalhamNaCasa": fields.Integer,
    "rendaMensalFamilia": fields.String,
    "programaGoverno": fields.String,
    "problemaEnfrentado": fields.Nested(problemasEnfrentadosFields)
}

class CondicaoVida(db.Model):
    __tablename__ = "tb_condicao_vida"

    problemaEnfrentado_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_problema_enfrentado.id"))

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trabalhoDaFamilia = db.Column(db.String, nullable=False)
    quantasPessoasTrabalhamNaCasa = db.Column(db.Integer, nullable=False)
    rendaMensalFamilia = db.Column(db.String, nullable=False)
    programaGoverno = db.Column(db.String, nullable=False)

    problemaEnfrentado = db.relationship("ProblemaEnfrentados", uselist=False, backref= db.backref("tb_problema_enfrentado", cascade="all, delete"))

    def __init__(self, trabalhoDaFamilia, quantasPessoasTrabalhamNaCasa, rendaMensalFamilia, programaGoverno, problemaEnfrentado):
        self.trabalhoDaFamilia = trabalhoDaFamilia
        self.quantasPessoasTrabalhamNaCasa = quantasPessoasTrabalhamNaCasa
        self.programaGoverno = programaGoverno
        self.rendaMensalFamilia = rendaMensalFamilia
        self.problemaEnfrentado = problemaEnfrentado

    def __repr__(self):
        return self
