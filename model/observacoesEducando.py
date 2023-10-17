from flask_restful import fields
from helpers.database import db
from model.deficiencia import deficienciaFields
from sqlalchemy.dialects.postgresql import UUID
import uuid

observacoesEducandoFields = {
    "id": fields.String,
    "alimentacao": fields.String,
    "medicacao": fields.String,
    "produtoHigienePessoal": fields.String,
    "tipoSangue": fields.String,
    "medicacaoDeficiencia": fields.String,
    "laudoMedico": fields.Boolean,
    "deficiencia": fields.Nested(deficienciaFields)
}

class ObservacoesEducando(db.Model):
    __tablename__ = "tb_observacoes_educando"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deficiencia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_deficiencia.id", ondelete='CASCADE'))

    alimentacao = db.Column(db.String, nullable=False)
    medicacao = db.Column(db.String, nullable=False)
    produtoHigienePessoal = db.Column(db.String, nullable=False)
    tipoSangue = db.Column(db.String, nullable=False)
    medicacaoDeficiencia = db.Column(db.String, nullable=False)
    laudoMedico = db.Column(db.Boolean, nullable=False)

    deficiencia = db.relationship("Deficiencia", cascade="all, delete", uselist=False, backref= db.backref("tb_deficiencia"))

    def __init__(self, alimentacao, medicacao, produtoHigienePessoal, tipoSangue, medicacaoDeficiencia, laudoMedico, deficiencia):
        self.alimentacao = alimentacao
        self.medicacao = medicacao
        self.produtoHigienePessoal = produtoHigienePessoal
        self.tipoSangue = tipoSangue
        self.medicacaoDeficiencia = medicacaoDeficiencia
        self.laudoMedico = laudoMedico
        self.deficiencia = deficiencia

    def __repr__(self):
        return self