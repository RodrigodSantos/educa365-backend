import re

def validateEmail(email):
  return re.match(r'[\w\.+-]+@([\w-]+\.)+[a-z]{2,}', email)

def validateCpf(cpf):
  return re.match(r'[0-9]{3}[.][0-9]{3}[.][0-9]{3}[-][0-9]{2}', cpf)

def validateRg(rg):
  return re.match(r'[0-9][.][0-9]{3}[.][0-9]{3}', rg)

def validateCep(cep):
  return re.match(r'[0-9]{5}[-][0-9]{3}', cep)

def validateTelefone(telefone):
  return re.match(r'[0-9]{11}', telefone)

def validateCnpj(cnpj):
  return re.match(r'\d{2}\.\d{3}\.\d{3}/0001-\d{2}', cnpj)