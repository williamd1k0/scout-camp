# -*- encoding: utf-8 -*-

from scoutcamp import *
from template import *
import argparse
import yaml

class ScoutCamp:

    __version__ = "Scout Camp 0.0.1"


    @staticmethod
    def main(**debug):
        if not debug:
            debug["path"] = ""

        configs = Config()
        teste = Template("list.yaml", debug["path"]+configs.get_path_to("templates"))

        print teste.get_template_list()
        print teste.get_templates()
        print teste


    @classmethod
    def debug(cls, path="testes/"):
        cls.main(**{"path":path})


    @staticmethod
    def myth():
        print "\n -*- Penso, logo mito -*-"


    @classmethod
    def get(cls, term):
        if(term == "version"):
            return cls.__version__


if __name__ == '__main__':
    #print help(argparse.ArgumentParser)
    parser = argparse.ArgumentParser(prog="Scout Camp", description="Scout Camp - Static HTML Group Manager")
    parser.add_argument("-d","--debug", help="run the debug mode")
    parser.add_argument("-m","--myth", help="myth", action="store_true")
    parser.add_argument("-v","--version", help="show version", action="store_true")
    args = parser.parse_args()

    if args.myth:
        ScoutCamp.myth()

    elif args.debug:
        ScoutCamp.debug()

    elif args.version:
        print ScoutCamp.get("version")
    else:
        ScoutCamp.main()
