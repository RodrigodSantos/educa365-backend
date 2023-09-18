from flask_restful import fields
from helpers.database import db

pessoaFeilds = {
    'id': fields.Integer,
    'nome': fields.String,
    'sexo': fields.String,
    'rg': fields.String,
    'cpf': fields.String,
    'dataNascimento': fields.String,
    'tipo': fields.String
}

class Pessoa(db.Model):
    __tablename__ = 'tbPessoa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    sexo = db.Column(db.String, nullable=False)
    rg = db.Column(db.String, nullable=False, unique=True)
    cpf = db.Column(db.String, nullable=False, unique=True)
    dataNascimento = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'pessoa',
        'polymorphic_on': tipo
    }

    def __init__(self, nome, sexo, rg, cpf, dataNascimento):
        self.nome = nome
        self.sexo = sexo
        self.rg = rg
        self.cpf = cpf
        self.dataNascimento = dataNascimento
    
    def __repr__(self):
        return f'<Pessoa {self.nome}>'
