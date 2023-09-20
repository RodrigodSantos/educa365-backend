from flask_restful import fields
from helpers.database import db

enderecoFields = {
    "id": fields.Integer,
    "rua": fields.String,
    "bairro": fields.String,
    "numero": fields.String,
    "uf": fields.String,
    "cidade": fields.String,
    "cep": fields.String,
    "telefone": fields.String,
    "referencia": fields.String
}

class Endereco(db.Model):
    __tablename__ = "tbEndereco"

    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String, nullable=False)
    bairro = db.Column(db.String, nullable=False)
    numero = db.Column(db.String, nullable=False)
    uf = db.Column(db.String, nullable=False)
    cidade = db.Column(db.String, nullable=False)
    cep = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=False)
    referencia = db.Column(db.String, nullable=False)

    def __init__(self, rua, bairro, numero, uf, cidade, cep, telefone, referencia):
        self.rua = rua
        self.bairro = bairro
        self.numero = numero
        self.uf = uf
        self.cidade = cidade
        self.cep = cep
        self.telefone = telefone
        self.referencia = referencia

    def __repr__(self):
        return self
