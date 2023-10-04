from flask_restful import fields
from helpers.database import db
from model.dateFormat import DateFormat
from model.pessoa import Pessoa
from model.endereco import enderecoFields
from model.turma import turmaFields
from model.instituicaoEnsino import instituicaoEnsinoFields
from model.observacoesEducando import observacoesEducandoFields
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

educandoFields = {
    "id": fields.String,
    'nome': fields.String,
    'sexo': fields.Boolean,
    'dataNascimento': DateFormat,
    'rg': fields.String,
    'cpf': fields.String,
    "nis": fields.String,
    "cidadeCartorio": fields.String,
    "sus": fields.String,
    "nomeCartorio": fields.String,
    "numeroRegistroNascimento": fields.String,
    "dataEmissaoCertidao": DateFormat,
    "ufCartorio": fields.String,
    "etnia": fields.String,
    "nomeMae": fields.String,
    "nomePai": fields.String,
    "dataMatricula": DateFormat,
    "endereco": fields.Nested(enderecoFields),
    "turma": fields.Nested(turmaFields),
    "instituicao": fields.Nested(instituicaoEnsinoFields),
    "observacoesEducando": fields.Nested(observacoesEducandoFields)
}

class Educando(Pessoa):
    __tablename__ = "tb_educando"

    pessoa_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_pessoa.id"), primary_key=True)
    turma_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_turma.id"))
    instituicao_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_instituicao_ensino.id"))
    observacoesEducando_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tb_observacoes_educando.id"))

    nis = db.Column(db.String, nullable=False)
    cidadeCartorio = db.Column(db.String, nullable=False)
    sus = db.Column(db.String, nullable=False)
    nomeCartorio = db.Column(db.String, nullable=False)
    numeroRegistroNascimento = db.Column(db.String, nullable=False)
    dataEmissaoCertidao = db.Column(db.DateTime, nullable=False)
    ufCartorio = db.Column(db.String, nullable=False)
    etnia = db.Column(db.String, nullable=False)
    nomeMae = db.Column(db.String, nullable=False)
    nomePai = db.Column(db.String, nullable=False)
    dataMatricula = db.Column(db.DateTime, default=datetime.datetime.now)

    __mapper_args__ = {"polymorphic_identity": "educando"}

    turma = db.relationship("Turma", uselist=False, backref= db.backref("tb_turma", cascade="all, delete"))
    instituicao = db.relationship("InstituicaoEnsino", uselist=False, backref= db.backref("tb_instituicao_ensino", cascade="all, delete"))
    observacoesEducando = db.relationship("ObservacoesEducando", uselist=False, backref= db.backref("tb_observacoes_educando", cascade="all, delete"))

    def __init__(self, nome, sexo, dataNascimento, rg, cpf, nis, cidadeCartorio, sus, nomeCartorio, numeroRegistroNascimento, dataEmissaoCertidao, ufCartorio, etnia, nomeMae, nomePai, observacoesEducando, endereco, turma, instituicao):
        super().__init__(nome, sexo, rg, cpf, dataNascimento, endereco)
        self.turma = turma
        self.instituicao = instituicao
        self.nis = nis
        self.cidadeCartorio = cidadeCartorio
        self.sus = sus
        self.nomeCartorio = nomeCartorio
        self.numeroRegistroNascimento = numeroRegistroNascimento
        self.dataEmissaoCertidao = dataEmissaoCertidao
        self.ufCartorio = ufCartorio
        self.etnia = etnia
        self.nomeMae = nomeMae
        self.nomePai = nomePai
        self.observacoesEducando = observacoesEducando

    def __repr__(self):
        return f'<Educando {self.nome}>'