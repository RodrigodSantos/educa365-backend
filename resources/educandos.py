from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid
import datetime

from model.educando import Educando, educandoFields
from model.endereco import Endereco
from model.instituicaoEnsino import InstituicaoEnsino
from model.observacoesEducando import ObservacoesEducando
from model.deficiencia import Deficiencia
from model.turma import Turma
from model.mensagem import Message, msgFields

parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("sexo", type=bool, help="Sexo não informado", required=True)
parser.add_argument("rg", type=str, help="Rg não informado", required=True)
parser.add_argument("cpf", type=str, help="Cpf não informado", required=True)
parser.add_argument("dataNascimento", type=str, help="Data de nascimento não informada", required=True)
parser.add_argument("nis", type=str, help="Nis não informado", required=True)
parser.add_argument("cidadeCartorio", type=str, help="Cidade do cartorio não informado", required=True)
parser.add_argument("sus", type=str, help="Sus não informado", required=True)
parser.add_argument("nomeCartorio", type=str, help="Nome Cartorio não informado", required=True)
parser.add_argument("numeroRegistroNascimento", type=str, help="Numero do registro de nascimento não informado", required=True)
parser.add_argument("dataEmissaoCertidao", type=str, help="Data de Emissao da Certidao não informado", required=True)
parser.add_argument("ufCartorio", type=str, help="Uf do Cartorio não informado", required=True)
parser.add_argument("etnia", type=str, help="Etnia não informada", required=True)
parser.add_argument("nomeMae", type=str, help="Nome da mae não informado", required=True)
parser.add_argument("nomePai", type=str, help="Nome do pai não informado", required=True)
parser.add_argument("ano", type=int, help="Ano não informado", required=True)
parser.add_argument("observacoesEducando", type=dict, help="Observacao do educando não informado", required=True)
parser.add_argument("endereco", type=dict, help="Telefone não informado", required=True)
parser.add_argument("turma", type=dict, help="Turma não informada", required=True)
parser.add_argument("instituicao", type=dict, help="Instituicao não informada", required=True)

class Educandos(Resource):
    def get(self):
        educandos = Educando.query.all()

        logger.info("Educandos listados com sucesso!")
        return marshal(educandos, educandoFields), 200

    def post(self):
        args = parser.parse_args()
        try:
            dataNascimento = args['dataNascimento'].split('-')
            dataNascimento = datetime.datetime(
                year=int(dataNascimento[0]),
                month=int(dataNascimento[1]),
                day=int(dataNascimento[2])
                )

            dataEmissaoCertidao = args['dataEmissaoCertidao'].split('-')
            dataEmissaoCertidao = datetime.datetime(
                year=int(dataEmissaoCertidao[0]),
                month=int(dataEmissaoCertidao[1]),
                day=int(dataEmissaoCertidao[2])
                )

            # Criacao de deficiencia
            deficiencia = Deficiencia(
                args['observacoesEducando']['deficiencia']['intelectual'],
                args['observacoesEducando']['deficiencia']['auditiva'],
                args['observacoesEducando']['deficiencia']['visual'],
                args['observacoesEducando']['deficiencia']['fisica'],
                args['observacoesEducando']['deficiencia']['multipla']
            )

            db.session.add(deficiencia)
            db.session.commit()
            logger.info(f"Deficiencia de id: {deficiencia.id} criado com sucesso")

            # Criacao das Observacoes do Educando
            observacoes = ObservacoesEducando(
                args['observacoesEducando']['alimentacao'],
                args['observacoesEducando']['medicacao'],
                args['observacoesEducando']['produtoHigienePessoal'],
                args['observacoesEducando']['tipoSangue'],
                args['observacoesEducando']['medicacaoDeficiencia'],
                args['observacoesEducando']['laudoMedico'],
                deficiencia
            )

            db.session.add(observacoes)
            db.session.commit()
            logger.info(f"ObservacaoEducando de id: {observacoes.id} criado com sucesso")

            # Criacao do Endereco
            endereco = Endereco(
                args['endereco']['rua'],
                args['endereco']['bairro'],
                args['endereco']['numero'],
                args['endereco']['uf'],
                args['endereco']['cidade'],
                args['endereco']['cep'],
                args['endereco']['telefone'],
                args['endereco']['referencia']
            )

            db.session.add(endereco)
            db.session.commit()
            logger.info(f"Endereco de id: {endereco.id} criado com sucesso")

            # Criacao da Turma
            turma = Turma(
                args['turma']['nome']
            )

            db.session.add(turma)
            db.session.commit()
            logger.info(f"Turma de id: {turma.id} criado com sucesso")

            # Criacao da instituicao
            instituicao = InstituicaoEnsino(
                args['instituicao']['nome'],
                args['instituicao']['cnpj']
            )

            db.session.add(instituicao)
            db.session.commit()
            logger.info(f"Instituicao de id: {instituicao.id} criado com sucesso")

            educando = Educando(
                args['nome'],
                args['sexo'],
                dataNascimento,
                args['rg'],
                args['cpf'],
                args['nis'],
                args['cidadeCartorio'],
                args['sus'],
                args['nomeCartorio'],
                args['numeroRegistroNascimento'],
                dataEmissaoCertidao,
                args['ufCartorio'],
                args['etnia'],
                args['nomeMae'],
                args['nomePai'],
                args['ano'],
                observacoes,
                endereco,
                turma,
                instituicao
            )

            db.session.add(educando)
            db.session.commit()

            logger.info(f"Educando de id: {educando.id} criado com sucesso")
            return marshal(educando, educandoFields), 200

        except:
            logger.error("Erro ao cadastrar o Educando")

            codigo = Message(2, "Erro ao cadastrar o Educando")
            return marshal(codigo, msgFields), 400


class EducandoId(Resource):
    def get(self, id):
        educando = Educando.query.get(uuid.UUID(id))

        if educando is None:
            logger.error(f"Educando de id: {id} não encontrado")

            codigo = Message(1, f"Educando de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404

        logger.info(f"Educando de id: {id} listado com sucesso!")
        return marshal(educando, educandoFields), 200

    def put(self, id):
        try:
            args = parser.parse_args()

            educando = Educando.query.get(uuid.UUID(id))

            if educando is None:
                logger.error(f"Educando de id: {id} não encontrado")

                codigo = Message(1, f"Educando de id: {id} não encontrado")
                return marshal(codigo, msgFields), 404

            observacoes = ObservacoesEducando.query.get(educando.observacoesEducando.id)
            deficiencia = Deficiencia.query.get(educando.observacoesEducando.deficiencia.id)
            endereco = Endereco.query.get(educando.endereco.id)
            turma = Turma.query.get(educando.turma.id)
            instituicao = InstituicaoEnsino.query.get(educando.instituicao.id)

            dataNascimento = args['dataNascimento'].split('-')
            dataNascimento = datetime.datetime(
                year=int(dataNascimento[0]),
                month=int(dataNascimento[1]),
                day=int(dataNascimento[2])
                )

            dataEmissaoCertidao = args['dataEmissaoCertidao'].split('-')
            dataEmissaoCertidao = datetime.datetime(
                year=int(dataEmissaoCertidao[0]),
                month=int(dataEmissaoCertidao[1]),
                day=int(dataEmissaoCertidao[2])
                )

            # Atualizacao de deficiencia
            deficiencia.intelectual = args['observacoesEducando']['deficiencia']['intelectual']
            deficiencia.auditiva = args['observacoesEducando']['deficiencia']['auditiva']
            deficiencia.visual = args['observacoesEducando']['deficiencia']['visual']
            deficiencia.fisica = args['observacoesEducando']['deficiencia']['fisica']
            deficiencia.multipla = args['observacoesEducando']['deficiencia']['multipla']

            db.session.add(deficiencia)
            db.session.commit()
            logger.info(f"Deficiencia de id: {deficiencia.id} atualizado com sucesso")

            # Atualizacao das Observacoes do Educando
            observacoes.alimentacao = args['observacoesEducando']['alimentacao']
            observacoes.medicacao = args['observacoesEducando']['medicacao']
            observacoes.produtoHigienePessoal = args['observacoesEducando']['produtoHigienePessoal']
            observacoes.tipoSangue = args['observacoesEducando']['tipoSangue']
            observacoes.medicacaoDeficiencia = args['observacoesEducando']['medicacaoDeficiencia']
            observacoes.laudoMedico = args['observacoesEducando']['laudoMedico']
            observacoes.deficiencia = deficiencia

            db.session.add(observacoes)
            db.session.commit()
            logger.info(f"ObservacaoEducando de id: {observacoes.id} atualizado com sucesso")

            # Atualizacao do Endereco
            endereco.rua = args['endereco']['rua']
            endereco.bairro = args['endereco']['bairro']
            endereco.numero = args['endereco']['numero']
            endereco.uf = args['endereco']['uf']
            endereco.cidade = args['endereco']['cidade']
            endereco.cep = args['endereco']['cep']
            endereco.telefone = args['endereco']['telefone']
            endereco.referencia = args['endereco']['referencia']

            db.session.add(endereco)
            db.session.commit()
            logger.info(f"Endereco de id: {endereco.id} atualizado com sucesso")

            # Atualizacao da Turma
            turma.nome = args['turma']['nome']

            db.session.add(turma)
            db.session.commit()
            logger.info(f"Turma de id: {turma.id} atualizado com sucesso")

            # Atualizacao da instituicao
            instituicao.nome = args['instituicao']['nome']
            instituicao.cnpj = args['instituicao']['cnpj']

            db.session.add(instituicao)
            db.session.commit()
            logger.info(f"Instituicao de id: {instituicao.id} atualizado com sucesso")

            # Atualizacao do Educando
            educando.nome = args['nome']
            educando.sexo = args['sexo']
            educando.dataNascimento = dataNascimento
            educando.rg = args['rg']
            educando.cpf = args['cpf']
            educando.nis = args['nis']
            educando.cidadeCartorio = args['cidadeCartorio']
            educando.sus = args['sus']
            educando.nomeCartorio = args['nomeCartorio']
            educando.numeroRegistroNascimento = args['numeroRegistroNascimento']
            educando.dataEmissaoCertidao = dataEmissaoCertidao
            educando.ufCartorio = args['ufCartorio']
            educando.etnia = args['etnia']
            educando.nomeMae = args['nomeMae']
            educando.nomePai = args['nomePai']
            educando.ano = args['ano']
            educando.observacoes = observacoes
            educando.endereco = endereco
            educando.turma = turma
            educando.instituicao = instituicao

            db.session.add(educando)
            db.session.commit()

            logger.info(f"Educando de id: {id} atalizado com sucesso!")
            return marshal(educando, educandoFields), 200

        except:
            logger.error("Error ao atualizar o Educando")

            codigo = Message(2, "Error ao atualizar o Educando")
            return marshal(codigo, msgFields), 400

    def delete(self, id):

        educando = Educando.query.get(uuid.UUID(id))

        if educando is None:
            logger.error(f"Educando de id: {id} não encontrado")

            codigo = Message(1, f"Educando de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404

        db.session.delete(educando)
        db.session.commit()

        logger.info(f"Educando de id: {id} deletedo com sucesso")
        return []
