# -*- encoding: utf-8 -*-


class ConfigException(Exception):

    def __init__(self, message="Configuration error"):
        print "ConfigException: "+message
