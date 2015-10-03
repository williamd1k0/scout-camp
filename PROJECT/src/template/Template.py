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
        template_list = []
        for i in temp_dict:
            template_list.append(temp_dict[i])
        self.__template_list = template_list[0]


    def get_template_list(self):
        return self.__template_list


    def __set_templates(self, path=None, extension=None):
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
        return self.__templates


    def to_string(self):
        return "".join(self.get_templates())


if __name__ == '__main__':

    print dir(Template)
    raw_input()
