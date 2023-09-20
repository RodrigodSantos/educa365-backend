from flask_restful import fields
from helpers.database import db
from model.endereco import enderecoFields


pessoaFeilds = {
    'id': fields.Integer,
    'nome': fields.String,
    'sexo': fields.String,
    'rg': fields.String,
    'cpf': fields.String,
    'dataNascimento': fields.DateTime,
    'tipo': fields.String,
    "endereco": fields.Nested(enderecoFields)
}

class Pessoa(db.Model):
    __tablename__ = 'tbPessoa'

    id = db.Column(db.Integer, primary_key=True)
    enderecoId = db.Column(db.Integer, db.ForeignKey("tbEndereco.id"))
    nome = db.Column(db.String, nullable=False)
    sexo = db.Column(db.String, nullable=False)
    rg = db.Column(db.String, nullable=False, unique=True)
    cpf = db.Column(db.String, nullable=False, unique=True)
    dataNascimento = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'pessoa',
        'polymorphic_on': tipo
    }

    endereco = db.relationship("Endereco", uselist=False, backref= db.backref("tbEndereco", cascade="all, delete"))

    def __init__(self, nome, sexo, rg, cpf, dataNascimento, endereco):
        self.nome = nome
        self.sexo = sexo
        self.rg = rg
        self.cpf = cpf
        self.dataNascimento = dataNascimento
        self.endereco = endereco

    def __repr__(self):
        return f'<Pessoa {self.nome}>'
