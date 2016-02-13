# -*- encoding: utf-8 -*-
from utils import Utils
printc = Utils.printc

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
