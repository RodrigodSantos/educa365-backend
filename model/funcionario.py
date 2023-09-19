from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa
from model.dateFormat import DateFormat
from model.endereco import enderecoFields

from model.endereco import Endereco

funcionarioFields = {
    "id": fields.Integer,
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
    __tablename__ = 'tbFuncionario'

    pessoaId = db.Column(db.Integer, db.ForeignKey("tbPessoa.id"), primary_key=True)
    enderecoId = db.Column(db.Integer, db.ForeignKey("tbEndereco.id"))
    email = db.Column(db.String, nullable=False, unique=True)
    cargo = db.Column(db.String, nullable=False)

    endereco = db.relationship("Endereco", uselist=False, backref= db.backref("tbEndereco", cascade="all, delete"))

    __mapper_args__ = {"polymorphic_identity": "funcionario"}

    def __init__(self, nome, sexo, rg, cpf, dataNascimento, email, cargo, endereco):
        super().__init__(nome, sexo, rg, cpf, dataNascimento)
        self.email = email
        self.cargo = cargo
        self.endereco = endereco

    def __repr__(self):
        return self