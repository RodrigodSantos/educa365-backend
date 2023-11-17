from datetime import datetime

def calcular_idade(data_nascimento):
    # Obtém a data atual
    hoje = datetime.now()

    # Calcula a diferença entre os anos
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

    return idade