# -*- encoding: utf-8 -*-

import yaml
import sys
from exceptions import LanguageException


class Lang(object):


    __lang_dict = None


    def __init__(self, path="", lang=None, ext=".yml"):

        try:
            lang_file = open(path+lang+ext, "r")
        except IOError:
            LanguageException("O arquivo de localização \"{0}{1}\" não foi encontrado!".format(lang,ext))
            sys.exit(1)

        lang_dict = yaml.load(lang_file.read())
        lang_file.close()

        self.__lang_dict = lang_dict


    def get_terms(self):
        return self.__lang_dict



if __name__ == '__main__':
    pass
