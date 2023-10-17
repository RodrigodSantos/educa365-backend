from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger
from sqlalchemy.exc import IntegrityError
from flask import request
from helpers.func.validations import *

import uuid
import datetime

# Educando
from model.educando import Educando, educandoFields
from model.endereco import Endereco
from model.instituicaoEnsino import InstituicaoEnsino
from model.observacoesEducando import ObservacoesEducando
from model.deficiencia import Deficiencia
from model.turma import Turma

# Responsavel
from model.responsavel import Responsavel
from model.bolsaFamilia import BolsaFamilia
from model.condicaoMoradia import CondicaoMoradia
from model.condicaoVida import CondicaoVida
from model.problemaEnfrentado import ProblemaEnfrentados

from model.educandoResponsavel import EducandoResponsavel, educandoResponsavelFields

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
parser.add_argument("turma_id", type=str, help="Turma não informada", required=False)
parser.add_argument("instituicao_id", type=str, help="Instituicao não informada", required=True)
parser.add_argument("endereco", type=dict, help="endereco não informado", required=False)
parser.add_argument("responsaveis", type=list, help="Responsavel não informado", required=False)
parser.add_argument("observacoesEducando", type=dict, help="observacoesEducando não informado", required=False)


class Educandos(Resource):
    def get(self):
        educandos = Educando.query.all()

        logger.info("Educandos listados com sucesso!")
        return marshal(educandos, educandoFields), 200

    def post(self):
        try:
            args = parser.parse_args()

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

            if validateCep(args['endereco']['cep']) == None:
                logger.error("Formato de cep não aceito")

                codigo = Message(2, "Formato de cep não aceito")
                return marshal(codigo, msgFields), 400

            elif validateTelefone(args['endereco']['telefone']) == None:
                logger.error("Formato de telefone não aceito")

                codigo = Message(2, "Formato de telefone não aceito")
                return marshal(codigo, msgFields), 400

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

            # Busca da Turma
            turma = Turma.query.get(args['turma_id'])

            if turma is None:
                logger.error(f"Turma de id: {id} não encontrada")

                codigo = Message(1, f"Turma de id: {id} não encontrada")
                return marshal(codigo, msgFields), 404

            # Busca da instituicao
            instituicao = InstituicaoEnsino.query.get(args['instituicao_id'])

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

            # Busca da Turma
            turma = Turma.query.get(args['turma_id'])

            if turma is None:
                logger.error(f"Turma de id: {id} não encontrada")

                codigo = Message(1, f"Turma de id: {id} não encontrada")
                return marshal(codigo, msgFields), 404

            # Busca da instituicao
            instituicao = InstituicaoEnsino.query.get(args['instituicao_id'])

            if instituicao is None:
                logger.error(f"Instituicao de Ensino de id: {id} não encontrada")

                codigo = Message(1, f"Instituicao de Ensino de id: {id} não encontrada")
                return marshal(codigo, msgFields), 404

            logger.info(f"Instituicao de id: {instituicao.id} criado com sucesso")

            if len(args['nome']) <= 2:
                logger.error("Nome do educando muito curto")

                codigo = Message(2, "Nome do educando muito curto")
                return marshal(codigo, msgFields), 400

            elif len(args['nomeMae']) <= 2:
                logger.error("Nome da mãe do educando muito curto")

                codigo = Message(2, "Nome da mãe do educando muito curto")
                return marshal(codigo, msgFields), 400

            elif len(args['nomePai']) <= 2:
                logger.error("Nome da pai do educando muito curto")

                codigo = Message(2, "Nome da pai do educando muito curto")
                return marshal(codigo, msgFields), 400

            if validateCpf(args['cpf']) == None:
                logger.error("Formato de cpf não aceito")

                codigo = Message(2, "Formato de cpf não aceito")
                return marshal(codigo, msgFields), 400

            elif validateRg(args['rg']) == None:
                logger.error("Formato de rg não aceito")

                codigo = Message(2, "Formato de rg não aceito")
                return marshal(codigo, msgFields), 400

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
                observacoes,
                endereco,
                turma,
                instituicao
            )

            db.session.add(educando)
            db.session.commit()
            logger.info(f"Educando de id: {educando.id} criado com sucesso")

            data = request.get_json()
            for i, responsavel in enumerate(data.get('responsaveis')):

                # Criacao BolsaFamilia
                if data.get('responsaveis')[i]['bolsaFamilia'] != None:
                    bolsaFamilia = BolsaFamilia(
                            data.get('responsaveis')[i]['bolsaFamilia']['nis']
                        )
                    db.session.add(bolsaFamilia)
                else:
                    bolsaFamilia = None

                # Criacao da Condicao da Moradia
                condicaoMoradia = CondicaoMoradia(
                    data.get('responsaveis')[i]['condicaoMoradia']['tipoCasa'],
                    data.get('responsaveis')[i]['condicaoMoradia']['posseCasa'],
                    data.get('responsaveis')[i]['condicaoMoradia']['banheiroComFossa'],
                    data.get('responsaveis')[i]['condicaoMoradia']['aguaCagepa'],
                    data.get('responsaveis')[i]['condicaoMoradia']['poco'],
                    data.get('responsaveis')[i]['condicaoMoradia']['energia']
                )

                db.session.add(condicaoMoradia)

                #Criacao ProblemaEnfrentado
                problemaEnfrentado = ProblemaEnfrentados(
                    data.get('responsaveis')[i]['condicaoVida']['problemaEnfrentado']['alcool'],
                    data.get('responsaveis')[i]['condicaoVida']['problemaEnfrentado']['lazer'],
                    data.get('responsaveis')[i]['condicaoVida']['problemaEnfrentado']['saude'],
                    data.get('responsaveis')[i]['condicaoVida']['problemaEnfrentado']['fome'],
                    data.get('responsaveis')[i]['condicaoVida']['problemaEnfrentado']['drogas'],
                    data.get('responsaveis')[i]['condicaoVida']['problemaEnfrentado']['violencia'],
                    data.get('responsaveis')[i]['condicaoVida']['problemaEnfrentado']['desemprego']
                )

                db.session.add(problemaEnfrentado)

                # Criacao Condicao de Vida
                condicaoVida = CondicaoVida(
                    data.get('responsaveis')[i]['condicaoVida']['trabalhoDaFamilia'],
                    data.get('responsaveis')[i]['condicaoVida']['quantasPessoasTrabalhamNaCasa'],
                    data.get('responsaveis')[i]['condicaoVida']['rendaMensalFamilia'],
                    data.get('responsaveis')[i]['condicaoVida']['programaGoverno'],
                    problemaEnfrentado
                )

                db.session.add(condicaoVida)

                # Criacao do Responsavel
                if len(data.get('responsaveis')[i]['nomeMae']) <= 2:
                    logger.error("Nome da mãe do responsavel muito curto")

                    codigo = Message(2, "Nome da mãe do responsavel muito curto")
                    return marshal(codigo, msgFields), 400

                if validateCpf(data.get('responsaveis')[i]['cpf']) == None:
                    logger.error("Formato de cpf não aceito")

                    codigo = Message(2, "Formato de cpf não aceito")
                    return marshal(codigo, msgFields), 400

                if validateRg(data.get('responsaveis')[i]['rg']) == None:
                    logger.error("Formato de rg não aceito")

                    codigo = Message(2, "Formato de rg não aceito")
                    return marshal(codigo, msgFields), 400


                responsavel = Responsavel(
                    data.get('responsaveis')[i]['nome'],
                    data.get('responsaveis')[i]['sexo'],
                    data.get('responsaveis')[i]['rg'],
                    data.get('responsaveis')[i]['cpf'],
                    data.get('responsaveis')[i]['dataNascimento'],
                    endereco,
                    data.get('responsaveis')[i]['parentesco'],
                    data.get('responsaveis')[i]['escolaridade'],
                    data.get('responsaveis')[i]['apelido'],
                    data.get('responsaveis')[i]['dataExpedicaoRg'],
                    data.get('responsaveis')[i]['dataExpedicaoCpf'],
                    data.get('responsaveis')[i]['profissao'],
                    data.get('responsaveis')[i]['nomeMae'],
                    data.get('responsaveis')[i]['ufRg'],
                    data.get('responsaveis')[i]['emissorRg'],
                    data.get('responsaveis')[i]['familiaresCasa'],
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

                responsaveisData = []
                educandosResponsaveis = EducandoResponsavel.query.filter_by(educando_id=educando.id).all()

                for educandoResponsavel in educandosResponsaveis:
                    responsavel = Responsavel.query.get(educandoResponsavel.responsavel_id)
                    responsaveisData.append(responsavel)

            data = {
                "id":educando.id,
                'nome':educando.nome,
                'sexo':educando.sexo,
                'dataNascimento': educando.dataNascimento,
                'rg':educando.rg,
                'cpf':educando.cpf,
                "nis":educando.nis,
                "cidadeCartorio":educando.cidadeCartorio,
                "sus":educando.sus,
                "nomeCartorio":educando.nomeCartorio,
                "numeroRegistroNascimento":educando.numeroRegistroNascimento,
                "dataEmissaoCertidao": educando.dataEmissaoCertidao,
                "ufCartorio":educando.ufCartorio,
                "etnia":educando.etnia,
                "nomeMae":educando.nomeMae,
                "nomePai":educando.nomePai,
                "dataMatricula": educando.dataMatricula,
                "endereco":educando.endereco,
                "turma":educando.turma,
                "instituicao":educando.instituicao,
                "observacoesEducando":educando.observacoesEducando,
                "responsaveis": responsaveisData
            }

            return marshal(data, educandoResponsavelFields), 200

        except IntegrityError:
            logger.error("Erro ao cadastrar o Educando - Email, cpf, Rg ou Nis ja cadastrado no sistema")

            codigo = Message(1, "Erro ao cadastrar o Educando - Email, cpf, Rg ou Nis ja cadastrado no sistema")
            return marshal(codigo, msgFields)

        except:
            logger.error("Erro ao cadastrar o Educando")

            codigo = Message(2, "Erro ao cadastrar o Educando")
            return marshal(codigo, msgFields), 400

class EducandoId(Resource):
    def get(self, id):
        responsaveisData = []
        educando = Educando.query.get(uuid.UUID(id))

        educandosResponsaveis = EducandoResponsavel.query.filter_by(educando_id=educando.id).all()

        for educandoResponsavel in educandosResponsaveis:
            responsavel = Responsavel.query.get(educandoResponsavel.responsavel_id)
            responsaveisData.append(responsavel)

        data = {
            "id":educando.id,
            'nome':educando.nome,
            'sexo':educando.sexo,
            'dataNascimento': educando.dataNascimento,
            'rg':educando.rg,
            'cpf':educando.cpf,
            "nis":educando.nis,
            "cidadeCartorio":educando.cidadeCartorio,
            "sus":educando.sus,
            "nomeCartorio":educando.nomeCartorio,
            "numeroRegistroNascimento":educando.numeroRegistroNascimento,
            "dataEmissaoCertidao": educando.dataEmissaoCertidao,
            "ufCartorio":educando.ufCartorio,
            "etnia":educando.etnia,
            "nomeMae":educando.nomeMae,
            "nomePai":educando.nomePai,
            "dataMatricula": educando.dataMatricula,
            "endereco":educando.endereco,
            "turma":educando.turma,
            "instituicao":educando.instituicao,
            "observacoesEducando":educando.observacoesEducando,
            "responsaveis": responsaveisData
        }

        if educando is None:
            logger.error(f"Educando de id: {id} não encontrado")

            codigo = Message(1, f"Educando de id: {id} não encontrado")
            return marshal(codigo, msgFields), 404

        logger.info(f"Educando de id: {id} listado com sucesso!")
        return marshal(data, educandoResponsavelFields), 200

    def put(self, id):
        try:
            args = parser.parse_args()

            educando = Educando.query.get(uuid.UUID(id))

            if educando is None:
                logger.error(f"Educando de id: {id} não encontrado")

                codigo = Message(1, f"Educando de id: {id} não encontrado")
                return marshal(codigo, msgFields), 404


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

            # Atualizacao da Turma
            turma_id = args['turma_id']
            turma = Turma.query.get(uuid.UUID(turma_id))
            db.session.add(turma)

            # Atualizacao da instituicao
            instituicao_id = args['instituicao_id']
            instituicao = InstituicaoEnsino.query.get(uuid.UUID(instituicao_id))
            db.session.add(instituicao)


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
            educando.turma = turma
            educando.instituicao = instituicao

            db.session.add(educando)
            db.session.commit()

            logger.info(f"Educando de id: {id} atalizado com sucesso!")
            return marshal(educando, educandoFields), 200

        except IntegrityError:
            logger.error("Erro ao cadastrar o Educando - Email, cpf, Rg ou Nis ja cadastrado no sistema")

            codigo = Message(1, "Erro ao cadastrar o Educando - Email, cpf, Rg ou Nis ja cadastrado no sistema")
            return marshal(codigo, msgFields)

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
