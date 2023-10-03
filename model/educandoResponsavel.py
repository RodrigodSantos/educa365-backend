from flask_restful import fields
from helpers.database import db

from model.educando import educandoFields
from model.responsavel import responsavelFields

import uuid

responsaveisFields = {
  "responsavel": fields.Nested(responsavelFields)
}

educandoResponsavelFields = {
  "educando": fields.Nested(educandoFields),
  "responsaveis": fields.Nested(responsaveisFields)
}

class EducandoResponsavel(db.Model):
    __tablename__ = "tb_educando_responsavel"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    educando_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_educando.pessoa_id"))
    responsavel_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_responsavel.pessoa_id"))

    educando = db.relationship("Educando", uselist=False, backref= db.backref("tb_educando", cascade="all, delete"))
    responsavel = db.relationship("Responsavel", uselist=False, backref= db.backref("tb_responsavel", cascade="all, delete"))

    def __init__(self, educando, responsavel):
        self.educando = educando
        self.responsavel = responsavel

    def __repr__(self):
        return self