from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa
from model.endereco import enderecoFields
from model.bolsaFamilia import bolsaFamiliaFields
from model.condicaoMoradia import condicaoMoradiaFields
from model.condicaoVida import condicaoVidaFields
from model.problemaEnfrentado import ProblemaEnfrentados

from model.dateFormat import DateFormat
from sqlalchemy.dialects.postgresql import UUID
import uuid

responsavelFields = {
    'id': fields.String,
    'nome': fields.String,
    'sexo': fields.Boolean,
    'rg': fields.String,
    'cpf': fields.String,
    'dataNascimento': DateFormat,
    "endereco": fields.Nested(enderecoFields),
    "parentesco": fields.String,
    "escolaridade": fields.String,
    "apelido": fields.String,
    "dataExpedicaoRg": DateFormat,
    "dataExpedicaoCpf": DateFormat,
    "profissao": fields.String,
    "nomeMae": fields.String,
    "ufRg": fields.String,
    "emissorRg": fields.String,
    "familiaresCasa": fields.Integer,
    "bolsaFamilia": fields.Nested(bolsaFamiliaFields),
    "condicaoMoradia": fields.Nested(condicaoMoradiaFields),
    "condicaoVida": fields.Nested(condicaoVidaFields)
}

class Responsavel(Pessoa):
    __tablename__ = "tb_responsavel"

    pessoa_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_pessoa.id"), primary_key=True)
    bolsaFamilia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_bolsa_familia.id"), nullable=True)
    condicaoMoradia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_condicao_moradia.id"), nullable=False)
    condicaoVida_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_condicao_vida.id"), nullable=False)

    parentesco = db.Column(db.String, nullable=False)
    escolaridade = db.Column(db.String, nullable=False)
    apelido = db.Column(db.String, nullable=False)
    dataExpedicaoRg = db.Column(db.DateTime, nullable=False)
    dataExpedicaoCpf = db.Column(db.DateTime, nullable=False)
    profissao = db.Column(db.String, nullable=False)
    nomeMae = db.Column(db.String, nullable=False)
    ufRg = db.Column(db.String, nullable=False)
    emissorRg = db.Column(db.String, nullable=False)
    familiaresCasa = db.Column(db.String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "responsavel"}

    bolsaFamilia = db.relationship("BolsaFamilia", uselist=False, backref=db.backref("tb_bolsa_familia", cascade="all, delete"))
    condicaoMoradia = db.relationship("CondicaoMoradia", uselist=False, backref=db.backref("tb_condicao_moradia", cascade="all, delete"))
    condicaoVida = db.relationship("CondicaoVida", uselist=False, backref=db.backref("tb_condicao_vida", cascade="all, delete"))

    def __init__(self, nome, sexo, rg, cpf, dataNascimento, endereco, parentesco, escolaridade, apelido, dataExpedicaoRg, dataExpedicaoCpf, profissao, nomeMae, ufRg, emissorRg, familiaresCasa, bolsaFamilia, condicaoMoradia, condicaoVida):
        super().__init__(nome, sexo, rg, cpf, dataNascimento, endereco)
        self.parentesco = parentesco
        self.escolaridade = escolaridade
        self.apelido = apelido
        self.dataExpedicaoRg = dataExpedicaoRg
        self.dataExpedicaoCpf = dataExpedicaoCpf
        self.profissao = profissao
        self.nomeMae = nomeMae
        self.ufRg = ufRg
        self.emissorRg = emissorRg
        self.familiaresCasa = familiaresCasa
        self.bolsaFamilia = bolsaFamilia
        self.condicaoMoradia = condicaoMoradia
        self.condicaoVida = condicaoVida

    def __repr__(self):
        return f'<Responsavel {self.nome}>'
