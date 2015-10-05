# -*- encoding: utf-8 -*-

from scoutcamp import *
from template import *
import argparse
import yaml

class ScoutCamp:

    @staticmethod
    def main():
        debug = "testes/"
        configs = Config()
        teste = Template("list.yaml",debug+configs.get_path_to("templates"))

        print teste.get_template_list()
        print teste.get_templates()
        print teste

    @staticmethod
    def myth():
        print "== Penso, logo mito =="

__version__ = "Scout Camp 0.0.1"

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--debug", help="init the debug mode.", action="store_true")
    parser.add_argument("-m","--myth", help="myth.", action="store_true")
    parser.add_argument("-v","--version", help="show version.", action="store_true")
    args = parser.parse_args()

    if args.myth:
        ScoutCamp.myth()

    elif args.debug:
        ScoutCamp.main()

    elif args.version:
        print __version__

    else:
        pass
