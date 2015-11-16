# -*- encoding: utf-8 -*-

import yaml
import sys
import sqlite3
from exceptions import *


class DataBase(object):

    __id = None
    __attributes = {}
    __relations = {}
    objects = []

    def __init__(self, path="", scout="", ext=".yml"):

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

        self.__class__.objects.append(self)


    def get_attributes(self):
        return self.__attributes

    def get_id(self):
        return self.__id

    def get_relations(self):
        return self.__relations

    @classmethod
    def all(cls):
        return cls.objects


class SQLite:

    connection = None
    __tables = []
    __inserts = []

    def __init__(self, database=None):

        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()


    def save(self):
        self.connection.commit()


    def close(self):
        self.connection.close()


    def new_column(self, name, c_type=None):

        if not c_type:
            c_type = "TEXT"
        table = "`"+name+"` "+c_type+","
        return table


    def new_table(self, columns=None, table=None, key=None):

        table_header = "CREATE TABLE \""+table+"\"("

        for attr in range(len(columns)):
            table_header += "\n\t"+self.new_column(columns[attr])

        table_header = table_header[0:len(table_header)-1]+")"

        self.__tables.append(table_header)

    def new_insert(self, table, attributes):

        insert_header = "INSERT INTO "+table+" ("
        for key in attributes.keys():
            insert_header += key+","

        insert_header = insert_header[0:len(insert_header)-1]+")\n VALUES ("
        for val in attributes.values():
            insert_header += "'"+str(val)+"',"

        insert_header = insert_header[0:len(insert_header)-1]+")"

        self.__inserts.append(insert_header)

    def crate_tables(self):
        for table in self.__tables:
            self.cursor.execute(table)

    def insert_into(self):
        for insert in self.__inserts:
            print insert
            self.cursor.execute(insert)


if __name__ == '__main__':
    pass
