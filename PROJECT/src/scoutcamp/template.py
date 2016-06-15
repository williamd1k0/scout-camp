# -*- encoding: utf-8 -*-

import yaml
from .database import *
from .exceptions import *


class Template(object):
    """Classe Template
        - Utilizada para obter e gerenciar a base dos templates.
        Atributos:
          - template_list (private:list): Lista de templates
          - templates (private:list): Templates
          - path (private:string): caminho para os arquivos
          - temp_extension (private:string): extensão dos arquivos de template
    """


    __template_list = None
    __templates = None
    __path = None
    __temp_extension = None


    def __init__(self, path="", list_file=None, extension=".html"):
        """Método construtor da Classe
            - Durante o instanciamento, os arquivos de lista e templates
            - são lidos e armazenados nos atributos específicos.
            Argumentos:
              - self (object): instância da própria classe
              - list_file (string): nome do arquivo da lista de templates (obrigatório)
              - path (string): caminho para o arquivo (default=string vazia)
              - extension (string): extensão opcional dos arquivos de template (default=".tmp")
            Retorno:
              - Sem retorno
        """

        # Previne instanciamento duplicado
        self.__template_list = DataList(path, list_file)
        self.__templates = list()

        # Seta um novo path caso seja diferete do padrão
        if path != self.__path:
            self.__path = path

        # Seta uma nova extensão caso seja diferente do padrão
        if extension != self.__temp_extension:
            self.__temp_extension = extension

        # Seta os templates a partir da lista
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
        # Percorre a dict para atribuir a uma list
        for i in temp_dict:
            template_list.append(temp_dict[i])
        # Atribui à nova lista somente a primeira posição da list
        self.__template_list = template_list[0]


    def get_template_list(self):
        """Método público get_template_list
            - Retorna a lista dos templates disponíveis.
            Argumentos:
              - self (object): instância da própria classe
            Retorno:
              - self.__template_list (lsit): lista de templates
        """
        return self.__template_list.get_data_list()


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
        # Se não foi definido um template, obtém do padrão
        if not path:
            path = self.__path
        # Se não foi definido uma extensão, obtém do padrão
        if not extension:
            extension = self.__temp_extension

        temps = []
        # Faz um loop pela lista de templates para obtê-los
        for i in self.get_template_list():
            try:
                template = open(path+i+extension,"r", encoding='utf-8')
                temps.append(template.read())
                template.close()

            except IOError:
                TemplateException("O arquivo "+i+extension+" não foi encontrado!")
                exit(1)

        # Seta o resultado no atriburo templates
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


    def __str__(self):
        """Método público
            - Retorna todos os templates em uma única string.
            Argumentos:
              - self (object): instância da própria classe
            Retorno:
              - self.__templates (string): templates em uma única string
        """
        # Junta todas as posições da list em uma string
        return str("".join(self.get_templates()))

    def __call__(self, term):
        if term == "string":
            return str(self)


if __name__ == '__main__':
    pass
