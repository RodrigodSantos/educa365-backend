from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa
from model.dateFormat import DateFormat
from model.endereco import enderecoFields
from sqlalchemy.dialects.postgresql import UUID

funcionarioFields = {
    "id": fields.String,
    "nome": fields.String,
    "sexo": fields.String,
    "rg": fields.String,
    "cpf": fields.String,
    "dataNascimento": DateFormat,
    "email": fields.String,
    "cargo": fields.String,
    "endereco": fields.Nested(enderecoFields)
}

class Funcionario(Pessoa):
    __tablename__ = 'tb_funcionario'

    pessoa_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_pessoa.id"), primary_key=True)

    email = db.Column(db.String, nullable=False, unique=True)
    cargo = db.Column(db.String, nullable=False)
    senha = db.Column(db.String, nullable=True)

    __mapper_args__ = {"polymorphic_identity": "funcionario"}

    def __init__(self, nome, sexo, rg, cpf, dataNascimento, endereco, email, cargo, senha):
        super().__init__(nome, sexo, rg, cpf, dataNascimento, endereco)
        self.email = email
        self.cargo = cargo
        self.senha = senha

    def __repr__(self):
        return f'<Funcionario {self.nome}>'