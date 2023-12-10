from datetime import datetime

def calcular_idade(data_nascimento):
    data_atual = datetime.now()

    nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    idade = data_atual.year - nascimento.year - ((data_atual.month, data_atual.day) < (nascimento.month, nascimento.day))

    return idade