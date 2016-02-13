# -*- encoding: utf-8 -*-
""" ScoutCamp API

-> modules
    ::config
        - Config
    ::database
        - DataList
        - DataBase
        - JsonParser
        - SQLiteExport
    ::server
        - Server
    ::lang
        - Lang
    ::template
        - Template
    ::utils
        - Utils
    ::exceptions
        - ConfigException
        - TemplateException
        - LanguageException
        - DataBaseException

-> dependencies
    ::yaml

"""

from config import Config
from database import *
from server import Server
from lang import Lang
from template import Template
from utils import Utils
from exceptions import *
