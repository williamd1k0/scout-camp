#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT PARA TESTAR OS MÉTODOS QUE SERÃO
USADOS OU NÃO NO PROJETO
"""
##- Module YAML -##
import yaml
# Utilizado para transformar uma string escrita
# em YAML para uma variável do tipo dict.
# TESTES: Funcionando como o esperado.

##- Module PyStache -##
import pystache
# Utilizado para o método do template, substituindo
# variáveis em uma string pelos valores obtidos no YAML.
# TESTES: Funcionando melhor que o esperado.


# Variáveis temporárias para definições.
# Posteriormente será obtivo via YAML.
path = "testes/"
template = "template.tmp"
strings = "pt_br.lang"

# Obtendo os arquivos com as strings e os templates.
lang = open(path+strings,"r")
temp = open(path+template,"r")

# Passando o template para uma string.
temp_base = temp.read()
lang_string = lang.read()

# Passando as strings em YAML para um 'dict'.
lang_dict = yaml.load(lang_string)

# Fechando arquivos.
lang.close()
temp.close()

# Criando instância do PyStache e inserindo as strings no template.
tempMaker = pystache.Renderer()
htmlBase = tempMaker.render(temp_base,lang_dict)

# Escrevendo o template pronto em um arquivo HTML.
teste = open(path+"teste.html","w")
teste.write(htmlBase.encode('utf8'))
teste.close()

# Somente printando as strings para testes.
print lang_dict
print "\n"
print htmlBase
print "\n"
print temp_base


##- Método file -##
# Usado para leitura/escrita de arquivos.
# TESTES: Funcionando mas depreciado.
# Usar 'open' ao invés de 'file'.
"""
lang = file("myth.js","w")
lang.write("coiso")
lang.write(str(json))
lang.close()
"""

raw_input()
