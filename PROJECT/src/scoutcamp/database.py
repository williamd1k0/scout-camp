# -*- encoding: utf-8 -*-

import yaml
import sys
import json
import sqlite3
from .exceptions import *


class DataList(object):


    __data_list = None


    def __init__(self, _path="", _list_file=""):

        self.__data_list = list()

        # Abre o arquivo da lista em YAML
        try:
            list_file = open(_path+_list_file,"r", encoding='utf-8')
        except IOError:
            DataBaseException("Não foi possível encontrar a lista \""+_path+_list_file+"\"!")
            sys.exit(1)

        # Passa o arquivo para uma dict
        yml_list = yaml.load(list_file.read())
        list_file.close()

        # Tenta converter a dict para uma list
        self.__set_data_list(yml_list)
        # Se falhar, lança uma exceção do template
        if type(self.__data_list) is not list:
            DataBaseException("Erro ao ler a lista \""+_path+_list_file+"\"!")


    def __set_data_list(self, temp_dict={}):
        """Método privado __set_data_list
            - Percorre uma dict para forçar que seja usada somente a
            - primeira posição e atribui o resultado ao atributo privado
            - __template_list (list).
            Argumentos:
              - self (object): instância da própria classe
              - temp_dict (dict): dict herdada do yaml (default=dict vazio)
            Retorno:
              - Sem retorno
        """
        temp_list = []
        # Percorre a dict para atribuir a uma list
        for i in temp_dict:
            temp_list.append(temp_dict[i])
        # Atribui à nova lista somente a primeira posição da list
        self.__data_list = temp_list[0]


    def get_data_list(self):
        """Método público get_data_list
            - Retorna a lista dos templates disponíveis.
            Argumentos:
              - self (object): instância da própria classe
            Retorno:
              - self.__data_list (list): lista de templates
        """
        return self.__data_list



class DataBase(object):


    __id = None
    __attributes = None
    __relations = None


    def __init__(self, path="", scout="", ext=".yml"):

        try:
            scout_file = open(path+scout+ext,'r', encoding='utf-8')
            scout_dict = yaml.load(scout_file.read())
            scout_file.close()
        except IOError:
            DataBaseException("Não foi possível encontrar o arquivo \""+path+scout+ext+"\"!")
            sys.exit(1)


        if "id" in scout_dict:
            self.__id = scout_dict["id"]

            # Previne instanciamento duplicado
            self.__attributes = dict()
            self.__relations = dict()

            for key in scout_dict.keys():
                if type(scout_dict[key]) is not list:
                    self.__attributes[key] = scout_dict[key]
                else:
                    self.__relations[key] = scout_dict[key]

        else:
            DataBaseException("O atributo id é obrigatório e não foi definido para {}".format(scout))
            sys.exit(1)


    def get_attributes(self):
        return self.__attributes


    def get_id(self):
        return self.__id


    def get_relations(self):
        return self.__relations




class JsonParser(object):


    __default_out = None
    __default_ext = None
    __default_indent = None


    def __init__ (self, _default_out, _default_ext=".json", _default_indent=8):
        self.__default_out = _default_out
        self.__default_ext = _default_ext
        self.__default_indent = _default_indent


    def to_json(self, _dict, _indent=None):
        if _indent is None:
            _indent = self.__default_indent
        return json.dumps(_dict, sort_keys=True, indent=_indent)


    def parse_list(self, _list):
        main_string = "{"
        for i in _list:
            main_string += '\n\t"'+i.get_id()+'":'

            main_dict = dict()
            main_dict.update(i.get_attributes())
            main_dict.update(i.get_relations())

            main_string += self.to_json(main_dict)
            main_string += ','

        main_string = main_string[0:len(main_string)-1]
        main_string += '\n}'
        return main_string


    def save(self, _json, _outfile, _alt_path=""):
        output = self.__default_out + _alt_path + _outfile+self.__default_ext

        json_output = open(output, "w", encoding='utf-8')
        json_output.write(_json)
        json_output.close()


    def save_all(self, _list, _outfile, _alt_path=""):
        self.save(self.parse_list(_list), _outfile, _alt_path)



class SQLiteExport(object):

    connection = None
    __tables = []
    __inserts = []

    def __init__(self, database=None):

        # Previne instanciamento duplicado
        self.__tables = list()
        self.__inserts = list()
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


    def new_table(self, columns=None, table=None, relationship=None):

        if relationship:
            table_header = "CREATE TABLE \""+table+"_"+relationship+"_relationship\"("
            table_header += "\n\t"+self.new_column(table+"_id")+"\n\t"+self.new_column(relationship+"_id")
        else:
            table_header = "CREATE TABLE \""+table+"\"("

            for attr in range(len(columns)):
                table_header += "\n\t"+self.new_column(columns[attr])

        table_header = table_header[0:len(table_header)-1]+")"

        self.__tables.append(table_header)


    def new_insert(self, table, attributes, relationship=None):

        if relationship:
            insert_header = "INSERT INTO "+table+"_"+relationship+"_relationship ("+table+"_id, "+relationship+"_id)\n VALUES ("
            insert_header += "'"+attributes[0]+"','"+attributes[1]+"',"
        else:
            insert_header = "INSERT INTO "+table+" ("

            for key in attributes.keys():
                insert_header += key+","

            insert_header = insert_header[0:len(insert_header)-1]+")\n VALUES ("
            for val in attributes.values():
                val = "%s" % val
                insert_header += "'%s'," % val

        insert_header = insert_header[0:len(insert_header)-1]+")"

        self.__inserts.append(insert_header)


    def crate_tables(self):
        for table in self.__tables:
            print(table)
            self.cursor.execute(table)


    def insert_into(self):
        for insert in self.__inserts:
            print(insert)
            self.cursor.execute(insert)


if __name__ == '__main__':
    pass
