from flask_restful import fields
from helpers.database import db
from model.deficiencia import deficienciaFields
from sqlalchemy.dialects.postgresql import UUID
import uuid


familiaresCasaFields = {
    "id": fields.String,
    "nome": fields.String,
    "parentesco": fields.String,
    "idade": fields.Integer,
    "estuda": fields.Boolean,
    "participaDaInstituicao": fields.Boolean,
    "turma": fields.String,
    "deficiencia": fields.Nested(deficienciaFields)
}

class FamiliaresCasa(db.Model):
    __tablename__ = "tb_familiares_casa"

    deficiencia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_deficiencia.id"))

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String, nullable=False)
    parentesco = db.Column(db.String, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    estuda = db.Column(db.Boolean, nullable=False)
    participaDaInstituicao = db.Column(db.Boolean, nullable=False)
    turma = db.Column(db.Boolean, nullable=False)

    deficiencia = db.relationship("Deficiencia", uselist=False, backref= db.backref("tb_deficiencia", cascade="all, delete"))

    def __init__(self, nome, parentesco, idade, estuda, participaDaInstituicao, turma, deficiencia):
        self.nome = nome
        self.parentesco = parentesco
        self.idade = idade
        self.estuda = estuda
        self.participaDaInstituicao = participaDaInstituicao
        self.turma = turma
        self.deficiencia = deficiencia

    def __repr__(self):
        return self
