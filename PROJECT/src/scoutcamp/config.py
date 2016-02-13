# -*- encoding: utf-8 -*-

import yaml
import sys
from database import *
from exceptions import *


class Config(object):


    __paths = {
        "templates": "_view",
        "table": "_table",
        "scouts": "_scouts",
        "badges": "_badges",
        "styles": "_styles",
        "scripts": "_js",
        "languages": "_lang",
        "index": "scout_board"
    }
    __build_paths = {
        "scripts": "js",
        "data": "data",
        "styles": "style"
    }
    __lists = {
        "templates": "list.yml",
        "scouts": "list.yml",
        "table": "list.yml",
        "badges": "list.yml",
        "scripts": "list.yml"
    }
    __terms = {
        "scouts": "scouts",
        "badges": "badges",
        "tiers": "tiers",
        "crests": "crests"
    }
    __server = {
        "host": "localhost",
        "port": 80
    }
    __camp = {
        "name": "Scout Camp"
    }
    __variables = {
        "badges": "badges",
        "scouts": "scouts",
        "custom": "custom"
    }

    __custom_variables = None

    __database = "scout"
    __language_list = None
    __current_language = "pt_br"
    __open_browser = True


    def __init__(self, config="conf.yml"):

        try:
            config_file = open(config, "r")
        except IOError:
            ConfigException("O arquivo \""+config+"\" para as configurações não foi encontrado!")
            sys.exit(1)
        config_dict = yaml.load(config_file.read())
        config_file.close()

        # Altera os padrões de host e porta a partir do arquivo de configuração
        if "server" in config_dict:
            if "host" in config_dict["server"]:
                self.__server["host"] = config_dict["server"]["host"]
            if "port" in config_dict["server"]:
                self.__server["port"] = config_dict["server"]["port"]


        if "camp" in config_dict:
            if "name" in config_dict["camp"]:
                self.__camp["name"] = config_dict["camp"]["name"]
            if "index" in config_dict["camp"]:
                self.__paths["index"] = config_dict["camp"]["index"]

        if "language_list" in config_dict:
            self.__language_list = DataList(self.get_path_to("languages"), config_dict["language_list"])

        if "current_language" in config_dict:
            self.__current_language = config_dict["current_language"]

        if "variables" in config_dict:
            if "scouts" in config_dict["variables"]:
                self.__variables["scouts"] = config_dict["variables"]["scouts"]
            if "badges" in config_dict["variables"]:
                self.__variables["badges"] = config_dict["variables"]["badges"]
            if "custom" in config_dict["variables"]:
                self.__variables["custom"] = config_dict["variables"]["custom"]

        if "custom_variables" in config_dict:
            self.__custom_variables = config_dict["custom_variables"]

        if "open_browser" in config_dict:
            self.__open_browser = config_dict["open_browser"]


    def __call__(self, cmd, args):
        pass


    def get_database(self):
        return self.__database


    def get_path_to(self, path):
        if self.__paths[path][-1] != "/":
            return self.__paths[path]+"/"
        else:
            return self.__paths[path]


    def get_build_path_to(self, path):
        if self.__build_paths[path][-1] != "/":
            return self.__build_paths[path]+"/"
        else:
            return self.__build_paths[path]


    def get_term(self, term):
        return self.__terms[term]


    def get_list_to(self, conf):
        return self.__lists[conf]


    def get_paths(self):
        return self.__paths


    def get_build_paths(self):
        return self.__build_paths


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


    def get_server_index(self):
        return self.__server["index"]


    def get_camp_name(self):
        return self.__camp["name"]


    def get_camp(self):
        return self.__camp


    def get_variable(self, var):
        return self.__variables[var]


    def get_all_variables(self):
        return self.__variables


    def get_custom_variables(self):
        return self.__custom_variables


    def get_language_list(self):
        return self.__language_list


    def get_current_language(self):
        return self.__current_language


    def get_open_browser(self):
        return self.__open_browser



if __name__ == '__main__':
    pass
