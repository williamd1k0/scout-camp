# -*- encoding: utf-8 -*-
from utils import Utils
prints = Utils.prints

class ConfigException(Exception):

    def __init__(self, message="Configuration error"):
        prints("\n ConfigException: "+message)


class TemplateException(Exception):

    def __init__(self, message="Template error"):
        prints("\n TemplateException: "+message)


class LanguageException(Exception):

    def __init__(self, message="Language error"):
        prints("\n LanguageException: "+message)


class DataBaseException(Exception):

    def __init__(self, message="DataBase error"):
        prints("\n DataBaseException: "+message)
