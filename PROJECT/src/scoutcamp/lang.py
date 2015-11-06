# -*- encoding: utf-8 -*-

import yaml
import sys
from exceptions import *

class Lang:

    __nav_buttons = {
        "badges": "Medalhas",
        "scouts": "Membros",
        "sort": "Ordenar",
        "select": "Selecionar Membro"
    }

    def __init__(self, path="", lang=None, ext=".lang"):

        try:
            lang_file = open(path+lang+ext, "r")
        except IOError:
            LanguageException("{0}{1} for template localization was not found".format(lang,ext))
            raw_input()
            sys.exit(1)

        lang_dict = yaml.load(lang_file.read())
        lang_file.close()

        if "nav_buttons" in lang_dict:
            for key_name in self.__nav_buttons.keys():
                if key_name in lang_dict["nav_buttons"]:
                    self.__nav_buttons[key_name] = lang_dict["nav_buttons"][key_name]


    def get_nav_buttons(self):
        return self.__nav_buttons

if __name__ == '__main__':
    pass
