# -*- encoding: utf-8 -*-

from scoutcamp import *
from template import *
import yaml

if __name__ == '__main__':

    teste = Template("list.yaml","testes/")
    print teste.get_template_list()
    print teste.get_templates()
    print teste.to_string()
    raw_input()
