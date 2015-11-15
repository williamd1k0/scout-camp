# -*- encoding: utf-8 -*-

import yaml
import sys
from exceptions import *


class DataBase:

    __id = None
    __attributes = {}

    def __init__(self, path="", scout=None, ext=".yml"):

        scout_file = open(path+scout+ext,'r')
        scout_dict = yaml.load(scout_file.read())
        scout_file.close()

        if "id" in scout_dict:

            self.__id = scout_dict["id"]

            for key in scout_dict.keys():
                self.__attributes[key] = scout_dict[key]


    def get_attributes(self):
        return self.__attributes

    def get_id(self):
        return self.__id


if __name__ == '__main__':
    pass
