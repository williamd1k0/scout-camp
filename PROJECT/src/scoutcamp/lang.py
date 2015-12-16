# -*- encoding: utf-8 -*-

import yaml
import sys
from exceptions import *


class Lang(object):


    __lang_dict = None

    def __init__(self, path="", lang=None, ext=".yml"):

        try:
            lang_file = open(path+lang+ext, "r")
        except IOError:
            LanguageException("{0}{1} for template localization was not found".format(lang,ext))
            raw_input()
            sys.exit(1)

        lang_dict = yaml.load(lang_file.read())
        lang_file.close()

        self.__lang_dict = lang_dict


    def get_lang(self):
        return self.__lang_dict

    def __dict__(self):
        return self.get_lang()


if __name__ == '__main__':
    pass
