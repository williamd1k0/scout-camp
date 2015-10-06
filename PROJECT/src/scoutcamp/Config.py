# -*- encoding: utf-8 -*-

import yaml
from exceptions import *

class Config:

    __paths = {
        "templates": "_view",
        "table": "_table",
        "scouts": "_scouts",
        "styles": "_styles",
        "scripts": "_js",
        "languages": "_lang"
    }
    __lists = {
        "templates": "list.yaml",
        "scouts": "list.yaml"
    }
    __facebook_mode = False

    def __init__(self, config_file="conf.yaml"):
        pass


    def __call__(self, cmd, args):
        pass


    def get_path_to(self, path):
        if self.__paths[path][-1] != "/":
            return self.__paths[path]+"/"
        else:
            return self.__paths[path]


    def get_list_to(self, conf):
        return self.__lists[conf]

    def get_paths(self):
        return self.__paths

    def get_lists(self):
        return self.__lists

    def list_paths(self):
        paths = ""
        for i in self.__paths:
            paths += self.__paths[i]+"\n"
        return paths

if __name__ == '__main__':

    teste = Config()
    print teste.get_path_to("template")
    print teste.get_paths()
    print teste.list_paths()
    raw_input()
