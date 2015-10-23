#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scoutcamp import *
import sys
import os
import yaml

class ScoutCamp:

    __version__ = "Scout Camp 0.0.2"


    @classmethod
    def main(cls, main_path=None, conf_override=None, mode="default", project_name=None):
        if not main_path:
            main_path = ""

        if conf_override:
            cls.configs = Config(conf_override)
        elif mode == "init":
            cls.configs = Config(init=True)
        else:
            cls.configs = Config()

        if mode == "server":
            cls.server()

        elif mode == "init":
            cls.init(project_name)

        else:
            try:
                teste = Template(cls.configs.get_list_to("templates"), main_path+cls.configs.get_path_to("templates"))

            except IOError:
                TemplateException("list.yml for templates not found")
                raw_input()
                sys.exit(1)

            print teste.get_template_list()
            print teste.get_templates()
            print teste

        sys.exit(0)


    @classmethod
    def use_alternative_path(cls, path=None):
        path = path.replace("\\","/")
        if path[-1] != "/":
            path += "/"
        os.chdir(path)
        cls.main()


    @classmethod
    def server(cls):
        camp = Server(cls.configs.get_server_host(),
                      cls.configs.get_server_port())
        os.chdir(cls.configs.get_server_index())
        camp.start_server()


    @staticmethod
    def myth():
        print "\n -*- Penso, logo mito -*-"


    @classmethod
    def get_version(cls):
        return cls.__version__

    @classmethod
    def init(cls, project_name):

        if not os.path.isdir(project_name):
            os.mkdir(project_name)
            os.chdir(project_name)

            for path in cls.configs.get_paths():
                os.mkdir(cls.configs.get_paths()[path])

            conf = open("conf.yml","w")
            conf.write( yaml.dump( dict(server = cls.configs.get_server()) ) )
            conf.close()

        else:
            print "The directory {} already exists!".format(project_name)

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(prog="ScoutCamp", description="Scout Camp - Static HTML Group Manager")
    parser.add_argument("-p","--path", help="compile using alternative path")
    parser.add_argument("-c","--create", help="create new ScoutCamp project")
    parser.add_argument("-t","--test", help="compile using another config file")
    parser.add_argument("-s","--server", help="start the Scout Camp server", action="store_true")
    parser.add_argument("-m","--myth", help=argparse.SUPPRESS, action="store_true")
    parser.add_argument("-v","--version", help="show version", action="store_true")
    args = parser.parse_args()

    if args.myth:
        ScoutCamp.myth()

    elif args.path:
        ScoutCamp.use_alternative_path(args.path)

    elif args.test and not args.server:
        ScoutCamp.main(conf_override=args.test)

    elif args.test and args.server:
        ScoutCamp.main(conf_override=args.test, mode="server")

    elif args.server and not args.test:
        ScoutCamp.main(mode="server")

    elif args.version:
        print ScoutCamp.get_version()

    elif args.create:
        print ScoutCamp.main(mode="init", project_name=args.create)

    else:
        ScoutCamp.main()
        raw_input()
