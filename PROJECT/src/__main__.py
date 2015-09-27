# -*- encoding: utf-8 -*-

from scoutcamp import *
from template import *
import yaml

path = "testes/"
teste = file(path+"william.scout","r")
obj = yaml.load(teste.read())
teste.close()

"""
teste = file("myth.js","w")

teste.write("coiso")
teste.write(str(json))
teste.close()
"""

coiso = Myth(obj["nome"])

print coiso.getNome()
