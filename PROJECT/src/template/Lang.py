# -*- encoding: utf-8 -*-

import yaml
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    
class Lang:

    BUTTONS = None
    EXCEPTIONS = None

    def __init__(self, lang=None,tlPath=None):

        try:
            obj = file(tlPath+"/"+lang+".lang","r")
        except:
            obj = None

        if obj:
            self.settings = yaml.load(obj)
            self.BUTTONS = self.settings["buttons"]
            self.EXCEPTIONS = self.settings["erros"]
