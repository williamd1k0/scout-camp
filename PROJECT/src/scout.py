#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scoutcamp import *
from template import *
import yaml

class ScoutCamp:

    __version__ = "Scout Camp 0.0.1"


    @staticmethod
    def main(debug_path=None, confoverride=None):
        if not debug_path:
            debug_path = ""
        if confoverride:
            configs = Config(confoverride)
        else:
            configs = Config()

        try:
            teste = Template(configs.get_list_to("templates"),
                             debug_path+configs.get_path_to("templates"))
        except IOError as ioe:
            TemplateException("list.yaml for templates not found")
            raw_input()
            exit(1)

        print teste.get_template_list()
        print teste.get_templates()
        print teste


    @staticmethod
    def debug(path="testes/"):
        path = path.replace("\\","/")
        if path[-1] != "/":
            path += "/"
        cls.main(debug_path=path)

    @staticmethod
    def server():
        camp = Server()
        camp.infinite()


    @staticmethod
    def myth():
        print "\n -*- Penso, logo mito -*-"


    @classmethod
    def get(cls, term):
        if(term == "version"):
            return cls.__version__


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(prog="Scout Camp", description="Scout Camp - Static HTML Group Manager")
    parser.add_argument("-d","--debug", help="run the debug mode")
    parser.add_argument("-c","--conf", help="use another config file")
    parser.add_argument("-s","--server", help="starts the Scout Camp server", action="store_true")
    parser.add_argument("-m","--myth", help="myth", action="store_true")
    parser.add_argument("-v","--version", help="show version", action="store_true")
    args = parser.parse_args()

    if args.myth:
        ScoutCamp.myth()

    elif args.debug:
        ScoutCamp.debug(args.debug)

    elif args.conf:
        ScoutCamp.main(confoverride=args.conf)

    elif args.server:
        ScoutCamp.server()

    elif args.version:
        print ScoutCamp.get("version")

    else:
        ScoutCamp.main()
        raw_input()
