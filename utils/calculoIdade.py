from datetime import datetime

def calcular_idade(data_nascimento):

    hoje = datetime.now()
    idade = (hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)))

    return idade