from flask_restful import fields
from helpers.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

deficienciaFields = {
    "id": fields.String,
    "intelectual": fields.Boolean,
    "auditiva": fields.Boolean,
    "visual": fields.Boolean,
    "fisica": fields.Boolean,
    "multipla": fields.Boolean,
}

class Deficiencia(db.Model):
    __tablename__ = "tb_deficiencia"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intelectual = db.Column(db.Boolean, nullable=False)
    auditiva = db.Column(db.Boolean, nullable=False)
    visual = db.Column(db.Boolean, nullable=False)
    fisica = db.Column(db.Boolean, nullable=False)
    multipla = db.Column(db.Boolean, nullable=False)

    def __init__(self, intelectual, auditiva, visual, fisica, multipla):
        self.intelectual = intelectual
        self.auditiva = auditiva
        self.visual = visual
        self.fisica = fisica
        self.multipla = multipla

    def __repr__(self):
        return self