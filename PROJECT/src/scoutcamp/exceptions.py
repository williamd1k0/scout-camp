# -*- encoding: utf-8 -*-
from .utils import *

printc = Utils.printc


class ScoutCampException(Exception):

    __error_log = ErrorLog()

    @classmethod
    def set_error_log(cls, _errlg):
        cls.__error_log = _errlg

    @classmethod
    def log(cls, info):
        cls.__error_log.log(info)


class ConfigException(Exception):

    def __init__(self, message="Configuration error"):
        printc("\n ConfigException: "+message, 'red')


class TemplateException(Exception):

    def __init__(self, message="Template error"):
        printc("\n TemplateException: "+message, 'red')


class LanguageException(Exception):

    def __init__(self, message="Language error"):
        printc("\n LanguageException: "+message, 'red')


class DataBaseException(Exception):

    def __init__(self, message="DataBase error"):
        printc("\n DataBaseException: "+message, 'red')


class ServerException(ScoutCampException):

    def __init__(self, message="Server error", err=''):
        ScoutCampException.log(err)
        printc("\n ServerException: "+message, 'red')



if __name__ == '__main__':
    pass
