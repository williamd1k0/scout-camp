#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scoutcamp import *
import platform
import sys, os
import yaml
import pystache


class ScoutCamp(object):

    __app__ = "ScoutCamp"
    __version__ = "0.5.1"
    __author__ = "William Tumeo <tumeowilliam@gmail.com>"
    configs = None
    main_template = None
    main_language = dict()


    @classmethod
    def main(cls, conf_override=None, mode="default", project_name=None):

        cls.progress('init')

        # Checagem para obter as configurações
        cls.progress('config_c')
        if conf_override:
            cls.configs = Config(conf_override)
        else:
            cls.configs = Config()

        # Iniciar servidor
        if mode == "server":
            cls.server()

        # Criar novo projeto
        elif mode == "init":
            cls.init(project_name)

        elif mode == "database":
            cls.generate_sql()

        else:
            # Compilar projeto
            cls.progress('folder_c')
            cls.check_folders()
            cls.compile()
            cls.progress('comp_end')

        sys.exit(0)


    @classmethod
    def check_folders(cls):
        base_paths = cls.configs.get_paths()
        build_paths = cls.configs.get_build_paths()
        build_main = base_paths['index']

        for folder in base_paths:
            if not os.path.isdir(base_paths[folder]):
                os.mkdir(base_paths[folder])

        for folder in build_paths:
            if not os.path.isdir(build_main+'/'+build_paths[folder]):
                os.mkdir(build_main+'/'+build_paths[folder])


    @classmethod
    def compile(cls):

        cls.progress('temp_c')
        try:
            # Templates base
            cls.main_template = Template(
                cls.configs.get_path_to("templates"),
                cls.configs.get_list_to("templates")
            )

        except IOError:
            raise
            TemplateException("list.yml for templates not found")
            raw_input()
            sys.exit(1)

        cls.progress('local_c')

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


################################################################################
        """Leitura e escrita das medalhas"""
        json_parser = JsonParser(cls.configs.get_path_to('index'))
        temp_terms = ['badges', 'scouts']

        for term in temp_terms:
            cls.progress('comp_term', cls.configs.get_term(term))
            badges_list = DataList(
                cls.configs.get_path_to(term),
                cls.configs.get_list_to(term),
            )

            cls.badge_base = list()

            for i in badges_list.get_data_list():
                cls.badge_base.append(DataBase(cls.configs.get_path_to(term), i))

            json_parser.save_all(cls.badge_base, cls.configs.get_term(term), cls.configs.get_build_path_to("data"))

################################################################################

        cls.progress('comp_page')
        temp_maker = pystache.Renderer()

        template_dict = dict()

        template_dict.update({"camp":cls.configs.get_camp()})
        template_dict.update(cls.main_language.get_lang())

        rendered_html = temp_maker.render(
            cls.main_template("string").decode('utf8'),
            template_dict
        )

        html_output = open(cls.configs.get_path_to("index") + "index.html","w")
        html_output.write(rendered_html.encode('utf8'))
        html_output.close()

        js_output = open(cls.configs.get_path_to("index")+"/js/"+"scoutboard.js","w")
        js_output.write("var scoutboard = document.querySelector('#scout-board');\nscoutboard.innerHTML = "+cls.main_scoutboard("string").encode('utf8')+";")
        js_output.close()



    """ Método generate_sql
    - Abandonado por enquanto
    """
    @classmethod
    def generate_sql(cls):

        data_base_file = cls.configs.get_path_to("index")+cls.configs.get_database()+".db"

        if os.path.exists(data_base_file):
            os.remove(data_base_file)

        table = SQLite(data_base_file)

        datas = ['flicky','william']
        teste_scout = []

        for i in datas:
            teste_scout.append(DataBase(cls.configs.get_path_to("scouts"), i))

        tables = ["scouts"]


        for new_table in tables:
            table.new_table(teste_scout[0].get_attributes().keys(), new_table)
            for relation in teste_scout[0].get_relations().keys():
                table.new_table(teste_scout[0].get_relations().keys(), "scouts", relation)
            table.crate_tables()
            for i in range(len(datas)):
                #teste_scout = DataBase(cls.configs.get_path_to("scouts"), i)
                #print scout.get_attributes()
                table.new_insert(new_table, teste_scout[i].get_attributes())

                for rel in teste_scout[i].get_relations().keys():
                    for rowid in teste_scout[i].get_relations()[rel]:
                        table.new_insert("scouts", [datas[i] , rowid], rel)


            table.insert_into()

        table.save()

        table.close()


    @classmethod
    def use_alternative_path(cls, path=None):
        path = path.replace("\\","/")
        if path[-1] != "/":
            path += "/"
        os.chdir(path)


    @classmethod
    def server(cls):
        camp = Server(cls.configs.get_server_host(),
                      cls.configs.get_server_port())
        os.chdir(cls.configs.get_path_to("index"))
        camp.start_server()


    @staticmethod
    def myth():
        # ninguém está vendo isso
        print("\n -*- Penso, logo mito -*-")


    @classmethod
    def get_version(cls):
        return cls.__version__

    @classmethod
    def get_app_name(cls):
        return cls.__app__

    @classmethod
    def get_author(cls):
        return cls.__author__


    @classmethod
    def get_full_version(cls):
        return cls.__app__+" "+cls.__version__+" "+cls.__author__


    @classmethod
    def progress(cls, prog=None, term=""):
        messages = {
            'init': " Inicializando...",
            'folder_c': " Checando pastas...",
            'config_c': " Checando configurações...",
            'temp_c': " Checando templates...",
            'local_c': " Checando localização...",
            'comp_term': " Compilando "+term+"...",
            'comp_page': " Compilando páginas...",
            'comp_end': " Compilação finalizada!"
        }
        print(messages[prog])


    @classmethod
    def init(cls, project_name):
        if not os.path.isdir(project_name):
            from zipfile import ZipFile
            with ZipFile(os.path.dirname(sys.argv[0])+'/base_project.zip', "r") as init_zip:
                init_zip.extractall(project_name)

        else:
            print("The directory {} already exists!".format(project_name))



if __name__ == '__main__':

    if sys.stdin.isatty():
        print("\n\n\t"+ScoutCamp.get_full_version())
        print("\n\tExecute pelo prompt/terminal!")
        raw_input()
        sys.exit()

    import argparse

    parser = argparse.ArgumentParser(prog="ScoutCamp", description="Scout Camp - Static HTML Group Manager")
    parser.add_argument("-r","--render", help="compile project using default config file", action="store_true")
    parser.add_argument("-p","--path", help="compile using alternative path")
    parser.add_argument("-c","--create", help="create new ScoutCamp project")
    parser.add_argument("-t","--test", help="compile using another config file")
    parser.add_argument("-s","--server", help="start the Scout Camp server", action="store_true")
    parser.add_argument("-d","--data", help="generate SQLite database", action="store_true")
    parser.add_argument("-m","--myth", help=argparse.SUPPRESS, action="store_true")
    parser.add_argument("-v","--version", help="show version", action="store_true")
    args = parser.parse_args()

    if args.myth:
        ScoutCamp.myth()

    if args.data:
        ScoutCamp.main(mode="database")

    elif args.path:
        ScoutCamp.use_alternative_path(args.path)

        if args.data:
            ScoutCamp.main(mode="database")

        elif args.render and not args.server:
            ScoutCamp.main()
            raw_input()
        elif args.server:
            ScoutCamp.main(mode="server")
        else:
            print("Use o comando path com render ou server!")
            raw_input()

    elif args.test and not args.server:
        ScoutCamp.main(conf_override=args.test)

    elif args.test and args.server:
        ScoutCamp.main(conf_override=args.test, mode="server")

    elif args.server and not args.test:
        ScoutCamp.main(mode="server")

    elif args.version:
        print(ScoutCamp.get_full_version())

    elif args.create:
        print(ScoutCamp.main(mode="init", project_name=args.create))

    elif args.render:
        ScoutCamp.main()
        raw_input()

    else:
        print(ScoutCamp.get_full_version())
        parser.print_help()
