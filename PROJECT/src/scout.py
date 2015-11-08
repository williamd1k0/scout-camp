#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scoutcamp import *
import platform
import sys
import os
import yaml
import pystache


class ScoutCamp:

    __version__ = "Scout Camp 0.2.1"
    configs = None
    main_template = None
    main_language = None


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
        cls.progress(3)

        try:
            # Templates base
            cls.main_template = Template(
                cls.configs.get_path_to("templates"),
                cls.configs.get_list_to("templates")
            )

        except IOError:
            TemplateException("list.yml for templates not found")
            raw_input()
            sys.exit(1)

        cls.progress(4)

        try:
            # Strings para localização
            cls.main_language = Lang(
                cls.configs.get_path_to("languages"),
                cls.configs.get_current_language()
            )

        except IOError:
            TemplateException("list.yml for locale not found")
            raw_input()
            sys.exit(1)

        try:
            # Template para a tabela de cada integrante
            cls.main_scoutboard = Template(
                cls.configs.get_path_to("table"),
                cls.configs.get_list_to("table")
            )

        except IOError:
            TemplateException("list.yml for scoutboard not found")
            raw_input()
            sys.exit(1)

        #print cls.main_template.get_template_list()
        #print cls.main_template.get_templates()
        #print cls.main_template

        cls.progress(5)
        temp_maker = pystache.Renderer()
        rendered_html = temp_maker.render(
            cls.main_template("string").decode('utf8'),
            dict(
                camp = cls.configs.get_camp(),
                nav_buttons = cls.main_language.get_nav_buttons()
            )
        )

        html_output = open(cls.configs.get_path_to("index") + "index.html","w")
        html_output.write(rendered_html.encode('utf8'))
        html_output.close()

        js_output = open(cls.configs.get_path_to("index")+"/js/"+"scoutboard.js","w")
        js_output.write("var scoutboard = document.querySelector('#scout-board');\nscoutboard.innerHTML = "+cls.main_scoutboard("string").encode('utf8')+";")
        js_output.close()


    @classmethod
    def use_alternative_path(cls, path=None):
        path = path.replace("\\","/")
        if path[-1] != "/":
            path += "/"
        os.chdir(path)
        #cls.main()


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
            from zipfile import ZipFile
            with ZipFile(os.path.dirname(sys.argv[0])+'/base_project.zip', "r") as init_zip:
                init_zip.extractall(project_name)

        else:
            print "The directory {} already exists!".format(project_name)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(prog="ScoutCamp", description="Scout Camp - Static HTML Group Manager")
    parser.add_argument("-r","--render", help="compile project using default config file", action="store_true")
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
        if args.render and not args.server:
            ScoutCamp.main()
            raw_input()
        elif args.server:
            ScoutCamp.main(mode="server")
        else:
            print "Use o comando path com render ou server!"
            raw_input()

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

    elif args.render:
        ScoutCamp.main()
        raw_input()

    else:
        parser.print_help()
