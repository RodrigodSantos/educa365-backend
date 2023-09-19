from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa
from model.dateFormat import DateFormat

funcionarioFields = {
    "id": fields.Integer,
    "nome": fields.String,
    "sexo": fields.String,
    "rg": fields.String,
    "cpf": fields.String,
    "dataNascimento": DateFormat,
    "email": fields.String,
    "cargo": fields.String
}

class Funcionario(Pessoa):
    __tablename__ = 'tbFuncionario'

    pessoaId = db.Column(db.Integer, db.ForeignKey("tbPessoa.id"), primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    cargo = db.Column(db.String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "funcionario"}

    def __init__(self, nome, sexo, rg, cpf, dataNascimento, email, cargo):
        super().__init__(nome, sexo, rg, cpf, dataNascimento)
        self.email = email
        self.cargo = cargo

    def __repr__(self):
        return self