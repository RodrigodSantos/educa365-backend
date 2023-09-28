from flask_restful import fields
from helpers.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

bolsaFamiliaFields = {
  "id": fields.String,
  "nis": fields.String
}

class BolsaFamilia(db.Model):
    __tablename__ = "tb_bolsa_familia"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nis = db.Column(db.String, nullable=False)

    def __init__(self, nis):
        self.nis = nis

    def __repr__(self):
        return self