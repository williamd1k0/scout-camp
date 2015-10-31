#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scoutcamp import *
import platform
import sys
import os
import yaml
import pystache


class ScoutCamp:

    __version__ = "Scout Camp 0.1.3"


    @classmethod
    def main(cls, conf_override=None, mode="default", project_name=None):

        cls.progress(1)

        # Checagem para obter as configurações
        cls.progress(2)
        if conf_override:
            cls.configs = Config(conf_override)
        elif mode == "init":
            cls.configs = Config(init=True)
        else:
            cls.configs = Config()

        # Iniciar servidor
        if mode == "server":
            cls.server()

        # Criar novo projeto
        elif mode == "init":
            cls.init(project_name)

        else:
            # Compilar projeto
            cls.compile()


        cls.progress()
        sys.exit(0)


    @classmethod
    def compile(cls):
        try:
            cls.progress(3)
            cls.main_template = Template(cls.configs.get_list_to("templates"), cls.configs.get_path_to("templates"))

        except IOError:
            TemplateException("list.yml for templates not found")
            raw_input()
            sys.exit(1)

        try:
            cls.progress(4)
            cls.main_language = Lang(cls.configs.get_path_to("languages"), cls.configs.get_current_language())

        except IOError:
            TemplateException("list.yml for templates not found")
            raw_input()
            sys.exit(1)

        #print cls.main_template.get_template_list()
        #print cls.main_template.get_templates()
        #print cls.main_template

        cls.progress(5)
        temp_maker = pystache.Renderer()
        htmlBase = temp_maker.render(
            cls.main_template("string").decode('utf8'),
            dict(
                camp = cls.configs.get_camp(),
                nav_buttons = cls.main_language.get_nav_buttons()
            )
        )

        teste = open(cls.configs.get_path_to("index") + "index.html","w")
        teste.write(htmlBase.encode('utf8'))
        teste.close()


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
        os.chdir(cls.configs.get_path_to("index"))
        camp.start_server()


    @staticmethod
    def myth():
        print "\n -*- Penso, logo mito -*-"


    @classmethod
    def get_version(cls):
        return cls.__version__

    @staticmethod
    def progress(prog=None):
        messages = [
            " Compilação finalizada!",
            " Inicializando...",
            " Checando configurações...",
            " Checando templates...",
            " Checando localização",
            " Compilando páginas..."
        ]
        if platform.system().lower() == "windows":
            for i in range(len(messages)):
                messages[i] = messages[i].decode("utf8")

        if prog:
            if prog == 1:
                print messages[prog]
            if prog == 2:
                print messages[prog]
            if prog == 3:
                print messages[prog]
            if prog == 4:
                print messages[prog]
            if prog == 5:
                print messages[prog]

        else:
            print messages[0]

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
