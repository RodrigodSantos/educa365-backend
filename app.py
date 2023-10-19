from flask import Flask
from flask_restful import Api
from helpers.database import db, migrate
from helpers.confCors import cors
import os
from dotenv import load_dotenv

from resources.funcionarios import Funcionarios, FuncionarioId
from resources.educandos import Educandos, EducandoId
from resources.enderecos import Enderecos, EnderecoId
from resources.instituicoes import Instituicoes, InstituicaoId
from resources.observacoesEducandos import ObservacoesEducandos, ObservacoesEducandoId
from resources.deficiencias import Deficiencias, DeficienciaId
from resources.turmas import Turmas, TurmaId
from resources.responsavel import Responsaveis, ResponsavelId
from resources.condicaoMoradia import CondicaoMoradias, CondicaoMoradiaId
from resources.condicaoVida import CondicaoVidas, CondicaoVidaId
from resources.EducandoResponsavel import EducandoResponsaveis

load_dotenv()

postgresUser = os.getenv("POSTGRES_USER")
postgresPassword = os.getenv("POSTGRES_PASSWORD")

app = Flask(__name__)

DB_URL = f"postgresql://{postgresUser}:{postgresPassword}@localhost:5432/Educa365"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
cors.init_app(app)
migrate.__init__(app, db)
api = Api(app)

# Funcionarios - Resource
api.add_resource(Funcionarios, '/funcionarios')
api.add_resource(FuncionarioId, '/funcionarios/<string:id>')

# Educandos - Resource
api.add_resource(Educandos, '/educandos')
api.add_resource(EducandoId, '/educandos/<string:id>')

# Enderecos - Resource
api.add_resource(Enderecos, '/enderecos')
api.add_resource(EnderecoId, '/enderecos/<string:id>')

# Instituicoes - Resource
api.add_resource(Instituicoes, '/instituicoes')
api.add_resource(InstituicaoId, '/instituicoes/<string:id>')

# Turmas - Resource
api.add_resource(Turmas, '/turmas')
api.add_resource(TurmaId, '/turmas/<string:id>')

# Observacoes do educando - Resource
api.add_resource(ObservacoesEducandos, '/observacoes')
api.add_resource(ObservacoesEducandoId, '/observacoes/<string:id>')

# Deficiencias do educando - Resource
api.add_resource(Deficiencias, '/deficiencias')
api.add_resource(DeficienciaId, '/deficiencias/<string:id>')

# Responsaveis
api.add_resource(Responsaveis, '/responsaveis')
api.add_resource(ResponsavelId, '/responsaveis/<string:id>')

# CondicaoMoradia
api.add_resource(CondicaoMoradias, '/condicaoMoradia')
api.add_resource(CondicaoMoradiaId, '/condicaoMoradia/<string:id>')

# CondicaoVida
api.add_resource(CondicaoVidas, '/condicaoVida')
api.add_resource(CondicaoVidaId, '/condicaoVida/<string:id>')

# EducandoResponsavel
api.add_resource(EducandoResponsaveis, '/educandoResponsaveis')

if __name__ == '__main__':
  app.run(debug=True)