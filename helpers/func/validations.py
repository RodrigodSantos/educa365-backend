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