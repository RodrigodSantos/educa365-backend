from flask_restful import fields
from helpers.database import db
from model.endereco import enderecoFields
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

pessoaFeilds = {
    'id': fields.Integer,
    'nome': fields.String,
    'sexo': fields.Boolean,
    'rg': fields.String,
    'cpf': fields.String,
    'dataNascimento': fields.DateTime,
    'tipo': fields.String,
    "endereco": fields.Nested(enderecoFields)
}

class Pessoa(db.Model):
    __tablename__ = 'tb_pessoa'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    endereco_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_endereco.id"))

    nome = db.Column(db.String, nullable=False)
    sexo = db.Column(db.Boolean, nullable=False)
    rg = db.Column(db.String, nullable=False, unique=True)
    cpf = db.Column(db.String, nullable=False, unique=True)
    dataNascimento = db.Column(db.DateTime, nullable=False)
    dataCriacao = db.Column(db.DateTime, default=datetime.datetime.now)
    tipo = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'pessoa',
        'polymorphic_on': tipo
    }

    endereco = db.relationship("Endereco", uselist=False, backref= db.backref("tb_endereco"))

    def __init__(self, nome, sexo, rg, cpf, dataNascimento, endereco):
        self.nome = nome
        self.sexo = sexo
        self.rg = rg
        self.cpf = cpf
        self.dataNascimento = dataNascimento
        self.endereco = endereco

    def __repr__(self):
        return f'<Pessoa {self.nome}>'
