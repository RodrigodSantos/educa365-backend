from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa

funcionarioFields = {
    "id": fields.Integer,
    "nome": fields.String,
    "sexo": fields.String,
    "rg": fields.String,
    "dataNascimento": fields.String,
    "email": fields.String,
    "cargo": fields.String
}

class Funcionario(Pessoa):
    __tablename__ = 'tbFuncionario'

    pessoaId = db.Column(db.Integer, db.ForeignKey("tbPessoa.id"), primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    cargo = db.Column(db.String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "funcionario"}

    def __init__(self, nome, sexo, rg, dataNascimento, email, cargo):
        super().__init__(nome, sexo, rg, dataNascimento)
        self.email = email
        self.cargo = cargo

    def __repr__(self):
        return self