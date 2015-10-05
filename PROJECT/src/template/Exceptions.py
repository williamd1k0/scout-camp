# -*- encoding: utf-8 -*-


class TemplateException(Exception):
    def __init__(self, message="Template error"):
        print "TemplateException: "+message
        exit()
