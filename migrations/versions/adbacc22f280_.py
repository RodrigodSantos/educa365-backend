"""empty message

Revision ID: adbacc22f280
Revises: 
Create Date: 2023-10-04 20:12:31.259938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adbacc22f280'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_bolsa_familia',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('nis', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_condicao_moradia',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('tipoCasa', sa.String(), nullable=False),
    sa.Column('posseCasa', sa.String(), nullable=False),
    sa.Column('banheiroComFossa', sa.Boolean(), nullable=False),
    sa.Column('aguaCagepa', sa.Boolean(), nullable=False),
    sa.Column('poco', sa.Boolean(), nullable=False),
    sa.Column('energia', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_deficiencia',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('intelectual', sa.Boolean(), nullable=False),
    sa.Column('auditiva', sa.Boolean(), nullable=False),
    sa.Column('visual', sa.Boolean(), nullable=False),
    sa.Column('fisica', sa.Boolean(), nullable=False),
    sa.Column('multipla', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_endereco',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('rua', sa.String(), nullable=False),
    sa.Column('bairro', sa.String(), nullable=False),
    sa.Column('numero', sa.String(), nullable=False),
    sa.Column('uf', sa.String(), nullable=False),
    sa.Column('cidade', sa.String(), nullable=False),
    sa.Column('cep', sa.String(), nullable=False),
    sa.Column('telefone', sa.String(), nullable=False),
    sa.Column('referencia', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_instituicao_ensino',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('cnpj', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_problema_enfrentado',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('alcool', sa.Boolean(), nullable=False),
    sa.Column('lazer', sa.Boolean(), nullable=False),
    sa.Column('saude', sa.Boolean(), nullable=False),
    sa.Column('fome', sa.Boolean(), nullable=False),
    sa.Column('drogas', sa.Boolean(), nullable=False),
    sa.Column('violencia', sa.Boolean(), nullable=False),
    sa.Column('desemprego', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_turma',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_condicao_vida',
    sa.Column('problemaEnfrentado_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('trabalhoDaFamilia', sa.String(), nullable=False),
    sa.Column('quantasPessoasTrabalhamNaCasa', sa.Integer(), nullable=False),
    sa.Column('rendaMensalFamilia', sa.String(), nullable=False),
    sa.Column('programaGoverno', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['problemaEnfrentado_id'], ['tb_problema_enfrentado.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_observacoes_educando',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('deficiencia_id', sa.UUID(), nullable=True),
    sa.Column('alimentacao', sa.String(), nullable=False),
    sa.Column('medicacao', sa.String(), nullable=False),
    sa.Column('produtoHigienePessoal', sa.String(), nullable=False),
    sa.Column('tipoSangue', sa.String(), nullable=False),
    sa.Column('medicacaoDeficiencia', sa.String(), nullable=False),
    sa.Column('laudoMedico', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['deficiencia_id'], ['tb_deficiencia.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_pessoa',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('endereco_id', sa.UUID(), nullable=True),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('sexo', sa.Boolean(), nullable=False),
    sa.Column('rg', sa.String(), nullable=False),
    sa.Column('cpf', sa.String(), nullable=False),
    sa.Column('dataNascimento', sa.DateTime(), nullable=False),
    sa.Column('dataCriacao', sa.DateTime(), nullable=True),
    sa.Column('tipo', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['endereco_id'], ['tb_endereco.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('rg')
    )
    op.create_table('tb_educando',
    sa.Column('pessoa_id', sa.UUID(), nullable=False),
    sa.Column('turma_id', sa.UUID(), nullable=True),
    sa.Column('instituicao_id', sa.UUID(), nullable=True),
    sa.Column('observacoesEducando_id', sa.UUID(), nullable=True),
    sa.Column('nis', sa.String(), nullable=False),
    sa.Column('cidadeCartorio', sa.String(), nullable=False),
    sa.Column('sus', sa.String(), nullable=False),
    sa.Column('nomeCartorio', sa.String(), nullable=False),
    sa.Column('numeroRegistroNascimento', sa.String(), nullable=False),
    sa.Column('dataEmissaoCertidao', sa.DateTime(), nullable=False),
    sa.Column('ufCartorio', sa.String(), nullable=False),
    sa.Column('etnia', sa.String(), nullable=False),
    sa.Column('nomeMae', sa.String(), nullable=False),
    sa.Column('nomePai', sa.String(), nullable=False),
    sa.Column('dataMatricula', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['instituicao_id'], ['tb_instituicao_ensino.id'], ),
    sa.ForeignKeyConstraint(['observacoesEducando_id'], ['tb_observacoes_educando.id'], ),
    sa.ForeignKeyConstraint(['pessoa_id'], ['tb_pessoa.id'], ),
    sa.ForeignKeyConstraint(['turma_id'], ['tb_turma.id'], ),
    sa.PrimaryKeyConstraint('pessoa_id')
    )
    op.create_table('tb_funcionario',
    sa.Column('pessoa_id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('cargo', sa.String(), nullable=False),
    sa.Column('senha', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['pessoa_id'], ['tb_pessoa.id'], ),
    sa.PrimaryKeyConstraint('pessoa_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('tb_responsavel',
    sa.Column('pessoa_id', sa.UUID(), nullable=False),
    sa.Column('bolsaFamilia_id', sa.UUID(), nullable=False),
    sa.Column('condicaoMoradia_id', sa.UUID(), nullable=False),
    sa.Column('condicaoVida_id', sa.UUID(), nullable=False),
    sa.Column('parentesco', sa.String(), nullable=False),
    sa.Column('escolaridade', sa.String(), nullable=False),
    sa.Column('apelido', sa.String(), nullable=False),
    sa.Column('dataExpedicaoRg', sa.DateTime(), nullable=False),
    sa.Column('ssp', sa.String(), nullable=False),
    sa.Column('dataExpedicaoCpf', sa.DateTime(), nullable=False),
    sa.Column('profissao', sa.String(), nullable=False),
    sa.Column('nomeMae', sa.String(), nullable=False),
    sa.Column('ufRg', sa.String(), nullable=False),
    sa.Column('emissorRg', sa.String(), nullable=False),
    sa.Column('familiaresCasa', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['bolsaFamilia_id'], ['tb_bolsa_familia.id'], ),
    sa.ForeignKeyConstraint(['condicaoMoradia_id'], ['tb_condicao_moradia.id'], ),
    sa.ForeignKeyConstraint(['condicaoVida_id'], ['tb_condicao_vida.id'], ),
    sa.ForeignKeyConstraint(['pessoa_id'], ['tb_pessoa.id'], ),
    sa.PrimaryKeyConstraint('pessoa_id')
    )
    op.create_table('tb_educando_responsavel',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('educando_id', sa.UUID(), nullable=True),
    sa.Column('responsavel_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['educando_id'], ['tb_educando.pessoa_id'], ),
    sa.ForeignKeyConstraint(['responsavel_id'], ['tb_responsavel.pessoa_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_educando_responsavel')
    op.drop_table('tb_responsavel')
    op.drop_table('tb_funcionario')
    op.drop_table('tb_educando')
    op.drop_table('tb_pessoa')
    op.drop_table('tb_observacoes_educando')
    op.drop_table('tb_condicao_vida')
    op.drop_table('tb_turma')
    op.drop_table('tb_problema_enfrentado')
    op.drop_table('tb_instituicao_ensino')
    op.drop_table('tb_endereco')
    op.drop_table('tb_deficiencia')
    op.drop_table('tb_condicao_moradia')
    op.drop_table('tb_bolsa_familia')
    # ### end Alembic commands ###
