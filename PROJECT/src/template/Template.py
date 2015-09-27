# -*- encoding: utf-8 -*-

from Lang import Lang

class Template:

    def __init__(self, lang=None,defaultTemplate=None):
        self.strings = Lang(lang)
