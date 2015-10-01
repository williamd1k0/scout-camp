# -*- encoding: utf-8 -*-

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from template import Lang

class Myth:

## Atributos ##

    __nome = None
    __faceID = None
    __joinDate = None
    __birthDate = None


    def __init__(self, nome=None, faceId=None, join_date=None, birthDate=None):
        """ Método Construtor
        :param nome:
        :param faceId:
        :param join_date:
        :param birthDate:
        """

        self.strings = Lang("pt_br","testes")

        if nome:
            self.__nome = nome
        else:
            print("Nome is not defined!")

## Métodos ##

    def setNome(self, nome):
        """ Método setNome
        :param nome:
        """
        self.__nome = nome

    def getNome(self):
        return self.__nome

    def setFaceID(self, face):
        self.__faceID = face

    def getFaceID(self):
        return self.__faceID

    def setJoinDate(self, date):
        self.__joinDate = date

    def getJoinDate(self):
        return self.__joinDate

    def setBirthDate(self, date):
        self.__birthDate = date

    def getBirthDate(self):
        return self.__birthDate


if __name__ == "__main__":

    print "\nClasse Myth\n"
    raw_input()
