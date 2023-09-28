from flask_restful import fields
from helpers.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

problemasEnfrentadosFields = {
    "id": fields.String,
    "alcool": fields.Boolean,
    "lazer": fields.Boolean,
    "saude": fields.Boolean,
    "fome": fields.Boolean,
    "drogas": fields.Boolean,
    "violencia": fields.Boolean,
    "desemprego": fields.Boolean
}

class ProblemaEnfrentados(db.Model):
    __tablename__ = "tb_problema_enfrentados"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alcool = db.Column(db.Boolean, nullable=False)
    lazer = db.Column(db.Boolean, nullable=False)
    saude = db.Column(db.Boolean, nullable=False)
    fome = db.Column(db.Boolean, nullable=False)
    drogas = db.Column(db.Boolean, nullable=False)
    violencia = db.Column(db.Boolean, nullable=False)
    desemprego = db.Column(db.Boolean, nullable=False)

    def __init__(self, alcool, lazer, saude, fome, drogas, violencia, desemprego):
        self.alcool = alcool
        self.lazer = lazer
        self.saude = saude
        self.fome = fome
        self.drogas = drogas
        self.violencia = violencia
        self.desemprego = desemprego

    def __repr__(self):
        return self