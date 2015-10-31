# -*- encoding: utf-8 -*-


class ConfigException(Exception):

    def __init__(self, message="Configuration error"):
        print "ConfigException: "+message


class TemplateException(Exception):

    def __init__(self, message="Template error"):
        print "TemplateException: "+message


class LanguageException(Exception):

    def __init__(self, message="Language error"):
        print "LanguageException: "+message
