from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger
from helpers.func.validations import *

import uuid

from model.bolsaFamilia import BolsaFamilia
from model.condicaoMoradia import CondicaoMoradia
from model.condicaoVida import CondicaoVida
from model.educando import Educando, educandoFields
from model.educandoResponsavel import EducandoResponsavel
from model.endereco import Endereco
from model.problemaEnfrentado import ProblemaEnfrentados
from model.responsavel import Responsavel, responsavelFields
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("sexo", type=bool, help="Sexo não informado", required=True)
parser.add_argument("rg", type=str, help="Rg não informado", required=True)
parser.add_argument("cpf", type=str, help="Cpf não informado", required=True)
parser.add_argument("dataNascimento", type=str, help="Data de Nascimento não informada", required=True)
parser.add_argument("endereco", type=dict, help="Endereco não informada", required=False)
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
parser.add_argument("condicaoMoradia", type=dict, help="condicaoMoradia não informado", required=False)
parser.add_argument("condicaoVida", type=dict, help="condicaoVida não informado", required=False)


class Responsaveis(Resource):
    def get(self):
        responsavel = Responsavel.query.all()

        logger.info("Responsaveis listados com sucesso!")
        return marshal(responsavel, responsavelFields), 200

class ResponsavelId(Resource):
    def post(self, id):
        args = parser.parse_args()
        educando = Educando.query.get(uuid.UUID(id))

        if args['bolsaFamilia'] != None:
            bolsaFamilia = BolsaFamilia(args['bolsaFamilia']['nis'])
            db.session.add(bolsaFamilia)
        else:
            bolsaFamilia = None

        # Criacao da Condicao da Moradia
        condicaoMoradia = CondicaoMoradia(
            args['condicaoMoradia']['tipoCasa'],
            args['condicaoMoradia']['posseCasa'],
            args['condicaoMoradia']['banheiroComFossa'],
            args['condicaoMoradia']['aguaCagepa'],
            args['condicaoMoradia']['poco'],
            args['condicaoMoradia']['energia']
        )

        db.session.add(condicaoMoradia)

        #Criacao ProblemaEnfrentado
        problemaEnfrentado = ProblemaEnfrentados(
            args['condicaoVida']['problemaEnfrentado']['alcool'],
            args['condicaoVida']['problemaEnfrentado']['lazer'],
            args['condicaoVida']['problemaEnfrentado']['saude'],
            args['condicaoVida']['problemaEnfrentado']['fome'],
            args['condicaoVida']['problemaEnfrentado']['drogas'],
            args['condicaoVida']['problemaEnfrentado']['violencia'],
            args['condicaoVida']['problemaEnfrentado']['desemprego']
        )

        db.session.add(problemaEnfrentado)

        # Criacao Condicao de Vida
        condicaoVida = CondicaoVida(
            args['condicaoVida']['trabalhoDaFamilia'],
            args['condicaoVida']['quantasPessoasTrabalhamNaCasa'],
            args['condicaoVida']['rendaMensalFamilia'],
            args['condicaoVida']['programaGoverno'],
            problemaEnfrentado
        )

        db.session.add(condicaoVida)

        if validateCpf(args['cpf']) == None:
            logger.error("Formato de cpf não aceito")

            codigo = Message(2, "Formato de cpf não aceito")
            return marshal(codigo, msgFields), 400

        elif validateRg(args['rg']) == None:
            logger.error("Formato de rg não aceito")

            codigo = Message(2, "Formato de rg não aceito")
            return marshal(codigo, msgFields), 400

        responsavel = Responsavel(
            args['nome'],
            args['sexo'],
            args['rg'],
            args['cpf'],
            args['dataNascimento'],
            educando.endereco,
            args['parentesco'],
            args['escolaridade'],
            args['apelido'],
            args['dataExpedicaoRg'],
            args['dataExpedicaoCpf'],
            args['profissao'],
            args['nomeMae'],
            args['ufRg'],
            args['emissorRg'],
            args['familiaresCasa'],
            bolsaFamilia,
            condicaoMoradia,
            condicaoVida
        )

        db.session.add(responsavel)

        # Add realcionamento Educando - Responsavel
        educandoResponsavel = EducandoResponsavel(
            educando,
            responsavel
        )

        db.session.add(educandoResponsavel)

        db.session.commit()

        return marshal(responsavel, responsavelFields), 200

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

    def delete(self, id):
        responsavel = Responsavel.query.get(uuid.UUID(id))

        if responsavel is None:
            logger.error(f"Responsavel de id: {id} não encontrado")

            codigo = Message(1, f"Responsavel de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404

        db.session.delete(responsavel)
        db.session.commit()

        logger.info(f"Responsavel de id: {id} deletedo com sucesso")
        return []
