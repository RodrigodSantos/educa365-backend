import uuid
from helpers.database import db
from flask_restful import fields

from model.relatorio import relatorioFields
from model.comentario import comentarioFields

comentarioRelatorioFields = {
    "relatorio": fields.Nested(relatorioFields),
    "comentario": fields.Nested(comentarioFields),
}

class ComentarioRelatorio(db.Model):
    __tablename__ = "tb_comentario_relatorio"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comentario_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_comentario.id"))
    relatorio_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_relatorio.id"))

    comentario = db.relationship("Comentario", uselist=False, backref=db.backref("tb_comentario"))
    relatorio = db.relationship("Relatorio", uselist=False, backref=db.backref("tb_relatorio"))

    def __init__(self, comentario_id, relatorio_id):
        self.comentario_id = comentario_id
        self.relatorio_id = relatorio_id

    def __repr__(self):
        return self