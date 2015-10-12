#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scoutcamp import *
from template import *
import sys
import yaml

class ScoutCamp:

    __version__ = "Scout Camp 0.0.1"


    @classmethod
    def main(cls, debug_path=None, confoverride=None, mode="default"):
        if not debug_path:
            debug_path = ""
        if confoverride:
            cls.configs = Config(confoverride)
        else:
            cls.configs = Config()

        if mode == "server":
            cls.server()
        else:
            try:
                teste = Template(cls.configs.get_list_to("templates"),
                                 debug_path+cls.configs.get_path_to("templates"))
            except IOError:
                TemplateException("list.yaml for templates not found")
                raw_input()
                sys.exit(1)

            print teste.get_template_list()
            print teste.get_templates()
            print teste

        sys.exit(0)


    @classmethod
    def debug(cls, path="testes/"):
        path = path.replace("\\","/")
        if path[-1] != "/":
            path += "/"
        cls.main(debug_path=path)


    @classmethod
    def server(cls):
        camp = Server(cls.configs.get_server_host(),
                      cls.configs.get_server_port())
        camp.start_server()


    @staticmethod
    def myth():
        print "\n -*- Penso, logo mito -*-"


    @classmethod
    def get(cls, term):
        if(term == "version"):
            return cls.__version__


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(prog="ScoutCamp", description="Scout Camp - Static HTML Group Manager")
    parser.add_argument("-d","--debug", help="run the debug mode")
    parser.add_argument("-c","--conf", help="use another config file")
    parser.add_argument("-s","--server", help="starts the Scout Camp server", action="store_true")
    parser.add_argument("-m","--myth", help=argparse.SUPPRESS, action="store_true")
    parser.add_argument("-v","--version", help="show version", action="store_true")
    args = parser.parse_args()

    if args.myth:
        ScoutCamp.myth()

    elif args.debug:
        ScoutCamp.debug(args.debug)

    elif args.conf:
        ScoutCamp.main(confoverride=args.conf)

    elif args.server:
        ScoutCamp.main(mode="server")

    elif args.version:
        print ScoutCamp.get("version")

    else:
        ScoutCamp.main()
        raw_input()
