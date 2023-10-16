from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid
from model.bolsaFamilia import BolsaFamilia
from model.condicaoMoradia import CondicaoMoradia
from model.condicaoVida import CondicaoVida
from model.problemaEnfrentado import ProblemaEnfrentados

from model.responsavel import Responsavel, responsavelFields
from model.endereco import Endereco
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("sexo", type=bool, help="Sexo não informado", required=True)
parser.add_argument("rg", type=str, help="Rg não informado", required=True)
parser.add_argument("cpf", type=str, help="Cpf não informado", required=True)
parser.add_argument("dataNascimento", type=str, help="Data de Nascimento não informada", required=True)
parser.add_argument("parentesco", type=str, help="Parentesco não informado", required=True)
parser.add_argument("escolaridade", type=str, help="Escolaridade não informada", required=True)
parser.add_argument("apelido", type=str, help="Apelido não informado", required=True)
parser.add_argument("dataExpedicaoRg", type=str, help="Data de expedicao do Rg não informado", required=True)
parser.add_argument("dataExpedicaoCpf", type=str, help="Data de expedicao do Cpf não informado", required=True)
parser.add_argument("profissao", type=str, help="Profissao não informado", required=True)
parser.add_argument("nomeMae", type=str, help="Nome da mae não informado", required=True)
parser.add_argument("ufRg", type=str, help="Uf do Rg não informado", required=True)
parser.add_argument("emissorRg", type=str, help="Emissor do Rg não informado", required=True)
parser.add_argument("familiaresCasa", type=int, help="Familiares da casa não informado", required=True)
parser.add_argument("bolsaFamilia", type=dict, help="bolsaFamilia não informado", required=False)


class Responsaveis(Resource):
    def get(self):
        responsavel = Responsavel.query.all()

        logger.info("Responsaveis listados com sucesso!")
        return marshal(responsavel, responsavelFields), 200

class ResponsavelId(Resource):
    def put(self, id):
        args = parser.parse_args()
        responsavel = Responsavel.query.get(uuid.UUID(id))

        if responsavel.bolsaFamilia != None:
            bolsaFamilia = BolsaFamilia.query.get(responsavel.bolsaFamilia.id)

            bolsaFamilia.nis = args['bolsaFamilia']['nis']
            db.session.add(bolsaFamilia)

        responsavel.nome = args['nome']
        responsavel.sexo = args['sexo']
        responsavel.rg = args['rg']
        responsavel.cpf = args['cpf']
        responsavel.dataNascimento = args['dataNascimento']
        responsavel.parentesco = args['parentesco']
        responsavel.escolaridade = args['escolaridade']
        responsavel.apelido = args['apelido']
        responsavel.dataExpedicaoRg = args['dataExpedicaoRg']
        responsavel.dataExpedicaoCpf = args['dataExpedicaoCpf']
        responsavel.profissao = args['profissao']
        responsavel.nomeMae = args['nomeMae']
        responsavel.ufRg = args['ufRg']
        responsavel.emissorRg = args['emissorRg']
        responsavel.familiaresCasa = args['familiaresCasa']
        responsavel.bolsaFamilia = bolsaFamilia

        db.session.add(responsavel)
        db.session.commit()

        logger.info(f"Responsavel de id: {id} atalizado com sucesso!")
        return marshal(responsavel, responsavelFields), 200
