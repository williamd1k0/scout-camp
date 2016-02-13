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
        "assets": "_assets",
        "scripts": "_js",
        "languages": "_lang",
        "index": "scout_board"
    }
    __build_paths = {
        "scripts": "js",
        "data": "data",
        "assets": "assets"
    }
    __lists = {
        "templates": "list.yml",
        "scouts": "list.yml",
        "table": "list.yml",
        "badges": "list.yml",
        "scripts": "list.yml"
    }
    __server = {
        "host": "localhost",
        "port": 80,
        "open_browser": True
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


    def __init__(self, config="conf.yml"):

        try:
            config_file = open(config, "r")
        except IOError:
            ConfigException("O arquivo \""+config+"\" para as configurações não foi encontrado!")
            sys.exit(1)
        config_dict = yaml.load(config_file.read())
        config_file.close()

        if "camp" in config_dict:
            if "name" in config_dict["camp"]:
                self.__camp["name"] = config_dict["camp"]["name"]
                if "index" in config_dict["camp"]:
                    self.__paths["index"] = config_dict["camp"]["index"]


        config_defaults = [
            ["server", ["host", "port", "open_browser"]],
            ["paths", ["templates", "scouts", "badges", "assets", "scripts", "languages"]],
            ["build_paths", ["scripts", "data", "assets"]],
            ["variables", ["scouts", "badges", "custom"]]
        ]

        # Setando todas as configurações que possuem o mesmo padrão
        for conf in config_defaults:
            if conf[0] in config_dict:
                for sett in conf[1]:
                    if sett in config_dict[conf[0]]:
                        if conf[0] == 'server':
                            self.__server[sett] = config_dict[conf[0]][sett]
                        elif conf[0] == 'paths':
                            self.__paths[sett] = config_dict[conf[0]][sett]
                        elif conf[0] == 'build_paths':
                            self.__build_paths[sett] = config_dict[conf[0]][sett]
                        elif conf[0] == 'variables':
                            self.__variables[sett] = config_dict[conf[0]][sett]


        if "language_list" in config_dict:
            self.__language_list = DataList(self.get_path_to("languages"), config_dict["language_list"])


        if "current_language" in config_dict:
            self.__current_language = config_dict["current_language"]


        if "custom_variables" in config_dict:
            self.__custom_variables = config_dict["custom_variables"]

        if "database" in config_dict:
            self.__database = config_dict["database"]



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
        return self.__server["open_browser"]



if __name__ == '__main__':
    pass
