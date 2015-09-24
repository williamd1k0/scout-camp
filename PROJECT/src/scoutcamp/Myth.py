# -*- encoding: utf-8 -*-

class Myth:

## Atributos ##

    __nome = None
    __faceId = None
    __joinDate = None

## Método Construtor ##

    def __init__(self, nome, join_date):
        pass

## Métodos ##

    def setNome(self, nome):
        self.__nome = nome

    def getNome(self):
        return self.__nome

if __name__ == "__main__":

    print "\nClasse Myth"
    raw_input()
