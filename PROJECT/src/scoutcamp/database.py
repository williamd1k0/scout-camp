# -*- encoding: utf-8 -*-

import yaml
import sys
import sqlite3
from exceptions import *


class DataBase:

    __id = None
    __attributes = {}
    __relations = {}

    def __init__(self, path="", scout=None, ext=".yml"):

        scout_file = open(path+scout+ext,'r')
        scout_dict = yaml.load(scout_file.read())
        scout_file.close()

        if "id" in scout_dict:

            self.__id = scout_dict["id"]

            for key in scout_dict.keys():
                if type(scout_dict[key]) is not list:
                    self.__attributes[key] = scout_dict[key]
                else:
                    self.__relations[key] = scout_dict[key]


    def get_attributes(self):
        return self.__attributes

    def get_id(self):
        return self.__id

    def get_relations(self):
        return self.__relations


class SQLite:

    @staticmethod
    def new_column(name, c_type=None):

        if not c_type:
            c_type = "TEXT"

        return "`"+name+"` "+c_type+","


class SQLiteTable:


    def __init__(self, columns=None, table=None, key=None):

        table_header = "CREATE TABLE \""+table+"\"("

        for attr in columns:
            table_header += "\n\t"+SQLite.new_column(attr)

        table_header = table_header[0:len(table_header)-1]+")"

        print table_header

        print table
        print key



if __name__ == '__main__':
    pass
