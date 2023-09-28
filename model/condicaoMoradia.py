from flask_restful import fields
from helpers.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

condicaoMoradiaFields = {
    "id": fields.String,
    "tipoCasa": fields.String,
    "banheiroComFossa": fields.Boolean,
    "aguaCagepa": fields.Boolean,
    "poco": fields.Boolean,
    "energia": fields.Boolean
}

class CondicaoMoradia(db.Model):
    __tablename__ = "tb_condicao_moradia"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipoCasa = db.Column(db.String, nullable=False)
    banheiroComFossa = db.Column(db.Boolean, nullable=False)
    aguaCagepa = db.Column(db.Boolean, nullable=False)
    poco = db.Column(db.Boolean, nullable=False)
    energia = db.Column(db.Boolean, nullable=False)

    def __init__(self, tipoCasa, banheiroComFossa, aguaCagepa, poco, energia):
        self.tipoCasa = tipoCasa
        self.banheiroComFossa = banheiroComFossa
        self.aguaCagepa = aguaCagepa
        self.poco = poco
        self.energia = energia

    def __repr__(self):
        return self