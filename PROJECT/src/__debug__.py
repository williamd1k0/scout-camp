#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import yaml

path = "testes/"
template = "template.tmp"
strings = "pt_br.lang"

lang = open(path+strings,"r")
temp = open(path+template,"r")
temp_base = temp.read()

lang_dict = yaml.load(lang.read())
lang.close()
temp.close()

"""
lang = file("myth.js","w")

lang.write("coiso")
lang.write(str(json))
lang.close()
"""

print lang_dict
print "\n"
print temp_base
raw_input()
