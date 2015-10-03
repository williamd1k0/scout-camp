# -*- encoding: utf-8 -*-

import yaml
from Exceptions import *

class Template:

    __template_list = None
    __templates = []
    __path = ""
    __temp_extension = ".tmp"

    def __init__(self, list_file, path="", extension=".tmp"):

        list_file = open(path+list_file,"r")
        template_list = yaml.load(list_file.read())
        list_file.close()

        self.__set_template_list(template_list)
        if type(self.__template_list) is not list:
            raise TemplateException("Template list have any typo.")

        if path != self.__path:
            self.__path = path

        if extension != self.__temp_extension:
            self.__temp_extension = extension

        self.__set_templates()


    def __set_template_list(self, temp_dict={}):
        """Método privado __set_template_list
            - Percorre uma dict para forçar que seja usada somente a
            - primeira posição e atribui o resultado ao atributo privado
            - __template_list (list).
            Argumentos:
              - self (object): instância da própria classe
              - temp_dict (dict): dict herdada do yaml (default=dict vazio)
            Retorno:
              - Sem retorno
        """
        template_list = []
        for i in temp_dict:
            template_list.append(temp_dict[i])
        self.__template_list = template_list[0]


    def get_template_list(self):
        """Método público get_template_list
            - Retorna a lista dos templates disponíveis.
            Argumentos:
              - self (object): instância da própria classe
            Retorno:
              - self.__template_list (lsit): lista de templates
        """
        return self.__template_list


    def __set_templates(self, path=None, extension=None):
        """Método privado __set_templates
            - Obtém os templates contidos na lista de templates e
            - atribui no atributo privado __templates (list).
            Argumentos:
              - self (object): instância da própria classe
              - path (string): caminho dos arquivos dos templates (default=None)
              - extension (string): extensão dos arquivos (default=None)
            Retorno:
              - Sem retorno
        """
        if not path:
            path = self.__path
        if not extension:
            extension = self.__temp_extension

        temps = []
        for i in self.get_template_list():
            template = open(path+i+extension,"r")
            temps.append(template.read())
            template.close()

        self.__templates = temps


    def get_templates(self):
        """Método público get_templates
            - Retorna todos os templates (list).
            Argumentos:
              - self (object): instância da própria classe
            Retorno:
              - self.__templates (list): lista com os templates
        """
        return self.__templates


    def to_string(self):
        """Método público
            - Retorna todos os templates em uma única string.
            Argumentos:
              - self (object): instância da própria classe
            Retorno:
              - self.__templates (string): templates em uma única string
        """
        return "".join(self.get_templates())


if __name__ == '__main__':

    print dir(Template)
    raw_input()
