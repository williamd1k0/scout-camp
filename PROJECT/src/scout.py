#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scoutcamp import *
import platform
import sys, os
import yaml
import pystache

prints = Utils.prints

class ScoutCamp(object):

    __app__ = "ScoutCamp"
    __version__ = "0.9.0"
    __author__ = "William Tumeo <tumeowilliam@gmail.com>"
    configs = None
    main_template = None
    main_language = None
    data_base = None
    languages = None


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
################################################################################
        """ Leitura dos templates """

        cls.progress('temp_c')

        # Templates base
        cls.main_template = Template(
            cls.configs.get_path_to("templates"),
            cls.configs.get_list_to("templates")
        )

        # Template para a tabela de cada integrante
        cls.main_scoutboard = Template(
            cls.configs.get_path_to("table"),
            cls.configs.get_list_to("table")
        )

        # Template de scripts
        cls.script_template = Template(
            cls.configs.get_path_to("scripts"),
            cls.configs.get_list_to("scripts"),
            ".js"
        )

        cls.progress('local_c')

        # Leitura das linguagens
        if cls.configs.get_language_list() is not None:
            languages = cls.configs.get_language_list().get_data_list()
        else:
            languages = [cls.configs.get_current_language()]

        cls.languages = dict()

        for lang in languages:
            cls.languages.update({lang: Lang(cls.configs.get_path_to("languages"), lang)})

        # Strings para localização
        cls.main_language = cls.languages[cls.configs.get_current_language()]


################################################################################
        """ Leitura e escrita dos membros e medalhas """

        json_parser = JsonParser(cls.configs.get_path_to('index'))
        temp_terms = ['badges', 'scouts']

        cls.data_base = dict()

        for term in temp_terms:
            cls.progress('comp_term', cls.configs.get_variable(term))

            badges_list = DataList(
                cls.configs.get_path_to(term),
                cls.configs.get_list_to(term),
            )

            badge_base = list()
            for i in badges_list.get_data_list():
                badge_base.append(DataBase(cls.configs.get_path_to(term), i))

            cls.data_base[cls.configs.get_variable(term)] = list()
            for row in badge_base:
                temp_data = dict()
                temp_data.update(row.get_attributes())
                temp_data.update(row.get_relations())
                cls.data_base[cls.configs.get_variable(term)].append(temp_data)

            json_parser.save_all(badge_base, cls.configs.get_variable(term), cls.configs.get_build_path_to("data"))

        cls.data_base[cls.configs.get_variable("custom")] = cls.configs.get_custom_variables()
        json_parser.save(json_parser.to_json(cls.configs.get_custom_variables(), 4), cls.configs.get_variable("custom"), cls.configs.get_build_path_to("data"))

################################################################################
        """ Template maker """

        cls.progress('comp_page')
        temp_maker = pystache.Renderer(string_encoding='utf8', escape=lambda a:a)

        template_dict = dict()
        template_dict.update({"camp":cls.configs.get_camp()})
        template_dict.update(cls.main_language.get_terms())
        template_dict.update(cls.data_base)

        rendered_board = temp_maker.render(
            cls.main_scoutboard("string").decode('utf8'),
            template_dict
        )

        template_dict.update({"table":rendered_board})

        rendered_html = temp_maker.render(
            cls.main_template("string").decode('utf8'),
            template_dict
        )

        html_output = open(cls.configs.get_path_to("index") + "index.html","w")
        html_output.write(rendered_html.encode('utf8'))
        html_output.close()

        for i in range(len(cls.script_template.get_templates())):
            rendered_script = temp_maker.render(
                cls.script_template.get_templates()[i].decode('utf8'),
                template_dict
            )
            js_output = open(cls.configs.get_path_to("index")+cls.configs.get_build_path_to("scripts")+cls.script_template.get_template_list()[i]+".js","w")
            js_output.write(rendered_script.encode('utf8'))
            js_output.close()



    """ Método generate_sql
    - Abandonado por enquanto
    """
    @classmethod
    def generate_sql(cls):

        data_base_file = cls.configs.get_path_to("index")+cls.configs.get_database()+".db"

        if os.path.exists(data_base_file):
            os.remove(data_base_file)

        table = SQLiteExport(data_base_file)

        ## NOTE: hard-coded
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
        camp = Server(
            cls.configs.get_server_host(),
            cls.configs.get_server_port(),
            cls.configs.get_open_browser()
        )
        os.chdir(cls.configs.get_path_to("index"))
        camp.start_server()


    @staticmethod
    def myth():
        # ninguém está vendo isso
        prints("\n -*- Penso, logo mito -*-")


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
        messages_unicode = {
            'init': " Inicializando...",
            'folder_c': " Checando pastas...",
            'config_c': " Checando configurações...",
            'temp_c': " Checando templates...",
            'local_c': " Checando localização...",
            'comp_term': " Compilando "+term+"...",
            'comp_page': " Compilando páginas...",
            'comp_end': " Compilação finalizada!"
        }
        try:
            prints(unicode(messages_unicode[prog], 'utf8'))
        except:
            prints(messages_unicode[prog])

    @classmethod
    def init(cls, project_name):
        if not os.path.isdir(project_name):
            from zipfile import ZipFile
            with ZipFile(os.path.dirname(sys.argv[0])+'/base_project.zip', "r") as init_zip:
                init_zip.extractall(project_name)

        else:
            prints("A pasta {} já existe!".format(project_name))



if __name__ == '__main__':

    # if sys.stdin.isatty():
    #     print("\n\n\t"+ScoutCamp.get_full_version())
    #     print("\n\tExecute pelo prompt/terminal!")
    #     raw_input()
    #     sys.exit()

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

        elif args.server:
            ScoutCamp.main(mode="server")
        else:
            prints("Use o comando path com render ou server!")

    elif args.test and not args.server:
        ScoutCamp.main(conf_override=args.test)

    elif args.test and args.server:
        ScoutCamp.main(conf_override=args.test, mode="server")

    elif args.server and not args.test:
        ScoutCamp.main(mode="server")

    elif args.version:
        prints(ScoutCamp.get_full_version())

    elif args.create:
        prints(ScoutCamp.main(mode="init", project_name=args.create))

    elif args.render:
        ScoutCamp.main()

    else:
        prints(ScoutCamp.get_full_version())
        parser.print_help()
