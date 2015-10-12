# -*- encoding: utf-8 -*-

import yaml
import sys
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
        "templates": "list.yml",
        "scouts": "list.yml"
    }
    __server = {
        "host": "localhost",
        "port": 80
    }
    __facebook_mode = False

    def __init__(self, config="conf.yml", init=False):

        if not init:

            try:
                config_file = open(config, "r")
            except IOError:
                ConfigException("conf.yml for settings was not found")
                raw_input()
                sys.exit(1)
            config_dict = yaml.load(config_file.read())

            # Altera os padrões de host e porta a partir do arquivo de configuração
            if "server" in config_dict:
                if "host" in config_dict["server"]:
                    self.__server["host"] = config_dict["server"]["host"]
                if "port" in config_dict["server"]:
                    self.__server["port"] = config_dict["server"]["port"]


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

    def get_server(self):
        return self.__server

    def list_paths(self):
        paths = ""
        for i in self.__paths:
            paths += self.__paths[i]+"\n"
        return paths

    def get_server_host(self):
        return self.__server["host"]

    def get_server_port(self):
        return self.__server["port"]


if __name__ == '__main__':

    teste = Config()
    print teste.get_path_to("template")
    print teste.get_paths()
    print teste.list_paths()
    raw_input()
