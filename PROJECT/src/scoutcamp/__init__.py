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
    ::download
        - TemplateUpdate
    ::utils
        - Utils
        - ErrorLog
    ::exceptions
        - ScoutCampException
        - ConfigException
        - TemplateException
        - LanguageException
        - DataBaseException
        - ServerException

-> dependencies
    ::yaml
    ::pystache
    ::colorama

"""

from config import Config
from database import *
from server import Server
from lang import Lang
from template import Template
from utils import *
from download import TemplateUpdate
from exceptions import *
