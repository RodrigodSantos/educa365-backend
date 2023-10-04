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
parser.add_argument("ssp", type=str, help="Ssp não informado", required=True)
parser.add_argument("dataExpedicaoCpf", type=str, help="Data de expedicao do Cpf não informado", required=True)
parser.add_argument("profissao", type=str, help="Profissao não informado", required=True)
parser.add_argument("nomeMae", type=str, help="Nome da mae não informado", required=True)
parser.add_argument("ufRg", type=str, help="Uf do Rg não informado", required=True)
parser.add_argument("emissorRg", type=str, help="Emissor do Rg não informado", required=True)
parser.add_argument("familiaresCasa", type=int, help="Familiares da casa não informado", required=True)
parser.add_argument("endereco", type=dict, help="Endereco não informado", required=True)
parser.add_argument("bolsaFamilia", type=dict, help="BolsaFamilia não informado", required=True)
parser.add_argument("condicaoMoradia", type=dict, help="Condicao Moradia não informado", required=True)
parser.add_argument("condicaoVida", type=dict, help="Condicao Vida não informado", required=True)

class Responsaveis(Resource):
    def get(self):
        responsavel = Responsavel.query.all()

        logger.info("Responsaveis listados com sucesso!")
        return marshal(responsavel, responsavelFields), 200

class ResponsavelId(Resource):
    def put(self, id):
        args = parser.parse_args()
        responsavel = Responsavel.query.get(uuid.UUID(id))

        # Put Endereco
        endereco = Endereco.query.get(responsavel.endereco.id)

        endereco.rua = args['endereco']['rua']
        endereco.bairro = args['endereco']['bairro']
        endereco.numero = args['endereco']['numero']
        endereco.uf = args['endereco']['uf']
        endereco.cidade = args['endereco']['cidade']
        endereco.cep = args['endereco']['cep']
        endereco.telefone = args['endereco']['telefone']
        endereco.referencia = args['endereco']['referencia']

        db.session.add(endereco)

        # Put Bolsa Familia
        bolsaFamilia = BolsaFamilia.query.get(responsavel.bolsaFamilia.id)

        bolsaFamilia.nis = args['bolsaFamilia']['nis']

        db.session.add(bolsaFamilia)

        # Put CondicaoMoradia
        condicaoMoradia = CondicaoMoradia.query.get(responsavel.condicaoMoradia.id)

        condicaoMoradia.tipoCasa = args['condicaoMoradia']['tipoCasa']
        condicaoMoradia.posseCasa = args['condicaoMoradia']['posseCasa']
        condicaoMoradia.banheiroComFossa = args['condicaoMoradia']['banheiroComFossa']
        condicaoMoradia.aguaCagepa = args['condicaoMoradia']['aguaCagepa']
        condicaoMoradia.poco = args['condicaoMoradia']['poco']
        condicaoMoradia.energia = args['condicaoMoradia']['energia']

        db.session.add(condicaoMoradia)

        # Put ProblemaEnfrentado
        problemaEnfrentado = ProblemaEnfrentados.query.get(responsavel.condicaoVida.problemaEnfrentado.id)

        problemaEnfrentado.alcool = args['condicaoVida']['problemaEnfrentado']['alcool']
        problemaEnfrentado.lazer = args['condicaoVida']['problemaEnfrentado']['lazer']
        problemaEnfrentado.saude = args['condicaoVida']['problemaEnfrentado']['saude']
        problemaEnfrentado.fome = args['condicaoVida']['problemaEnfrentado']['fome']
        problemaEnfrentado.drogas = args['condicaoVida']['problemaEnfrentado']['drogas']
        problemaEnfrentado.violencia = args['condicaoVida']['problemaEnfrentado']['violencia']
        problemaEnfrentado.desemprego = args['condicaoVida']['problemaEnfrentado']['desemprego']

        db.session.add(problemaEnfrentado)

        # Put CondicaoVida
        condicaoVida = CondicaoVida.query.get(responsavel.condicaoVida.id)

        condicaoVida.trabalhoDaFamilia = args['condicaoVida']['trabalhoDaFamilia']
        condicaoVida.quantasPessoasTrabalhamNaCasa = args['condicaoVida']['quantasPessoasTrabalhamNaCasa']
        condicaoVida.rendaMensalFamilia = args['condicaoVida']['rendaMensalFamilia']
        condicaoVida.programaGoverno = args['condicaoVida']['programaGoverno']
        condicaoVida.problemaEnfrentado = problemaEnfrentado

        db.session.add(condicaoVida)

        responsavel.nome = args['nome']
        responsavel.sexo = args['sexo']
        responsavel.rg = args['rg']
        responsavel.cpf = args['cpf']
        responsavel.dataNascimento = args['dataNascimento']
        responsavel.parentesco = args['parentesco']
        responsavel.escolaridade = args['escolaridade']
        responsavel.apelido = args['apelido']
        responsavel.dataExpedicaoRg = args['dataExpedicaoRg']
        responsavel.ssp = args['ssp']
        responsavel.dataExpedicaoCpf = args['dataExpedicaoCpf']
        responsavel.profissao = args['profissao']
        responsavel.nomeMae = args['nomeMae']
        responsavel.ufRg = args['ufRg']
        responsavel.emissorRg = args['emissorRg']
        responsavel.familiaresCasa = args['familiaresCasa']

        db.session.add(responsavel)
        db.session.commit()

        logger.info(f"Responsavel de id: {id} atalizado com sucesso!")
        return marshal(responsavel, responsavelFields), 200
