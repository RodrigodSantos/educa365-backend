from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa
from model.endereco import enderecoFields
from model.bolsaFamilia import bolsaFamiliaFields
from model.dateFormat import DateFormat
from sqlalchemy.dialects.postgresql import UUID
import uuid


responsavelFields = {
    'id': fields.String,
    'nome': fields.String,
    'sexo': fields.Boolean,
    'rg': fields.String,
    'cpf': fields.String,
    'dataNascimento': fields.DateTime,
    "endereco": fields.Nested(enderecoFields),
    "parentesco": fields.String,
    "escolaridade": fields.String,
    "apelido": fields.String,
    "dataExpedicaoRg": DateFormat,
    "ssp": fields.String,
    "dataExpedicaoCpf": DateFormat,
    "profissao": fields.String,
    "nomeMae": fields.String,
    "ufRg": fields.String,
    "emissorRg": fields.String,
    "bolsaFamilia": fields.Nested(bolsaFamiliaFields)
}

class Responsavel(Pessoa):
    _tablename__ = 'tb_responsavel'

    pessoa_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_pessoa.id"), primary_key=True)
    bolsaFamilia_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_bolsaFamilia.id"), nullable=False)

    nome = db.Column(db.String, nullable=False)
    sexo = db.Column(db.Boolean, nullable=False)
    rg = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String, nullable=False)
    dataNascimento = db.Column(db.DateTime, nullable=False)
    parentesco = db.Column(db.String, nullable=False)
    escolaridade = db.Column(db.String, nullable=False)
    apelido = db.Column(db.String, nullable=False)
    dataExpedicaoRg = db.Column(db.DateTime, nullable=False)
    ssp = db.Column(db.String, nullable=False)
    dataExpedicaoCpf = db.Column(db.DateTime, nullable=False)
    profissao = db.Column(db.String, nullable=False)
    nomeMae = db.Column(db.String, nullable=False)
    ufRg = db.Column(db.String, nullable=False)
    emissorRg = db.Column(db.String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "responsavel"}

    bolsaFamilia = db.relationship("BolsaFamilia", uselist=False, backref= db.backref("tb_bolsaFamilia", cascade="all, delete"))

    def __init__(self, nome, sexo, rg, cpf, dataNascimento, endereco, parentesco, escolaridade, apelido, dataExpedicaoRg, ssp, dataExpedicaoCpf, profissao, nomeMae, ufRg, emissorRg, bolsaFamilia):
        super().__init__(nome, sexo, rg, cpf, dataNascimento, endereco)
        self.parentesco = parentesco
        self.escolaridade = escolaridade
        self.apelido = apelido
        self.dataExpedicaoRg = dataExpedicaoRg
        self.ssp = ssp
        self.dataExpedicaoCpf = dataExpedicaoCpf
        self.profissao = profissao
        self.nomeMae = nomeMae
        self.ufRg = ufRg
        self.emissorRg = emissorRg
        self.bolsaFamilia = bolsaFamilia

    def __repr__(self):
        return f'<Responsavel {self.nome}>'
