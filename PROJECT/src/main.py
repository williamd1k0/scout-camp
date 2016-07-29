#!/usr/bin/python
# -*- encoding: utf-8 -*-

import yaml
import pystache
import jinja2 as jinjo
import colorama
import shutil, sys, os
from scoutcamp import *
from distutils.dir_util import copy_tree

prints = Utils.prints
printc = Utils.printc
paint = Utils.paint


class ScoutCamp(object):


    __app__ = "ScoutCamp"
    __version__ = "1.2.0"
    __author__ = "William Tumeo <tumeowilliam@gmail.com>"
    program_path = None
    configs = None
    main_template = None
    main_language = None
    data_base = None
    languages = None


    @classmethod
    def main(cls, conf_override=None, mode="default", project_name=None):

        cls.progress('init')
        cls.program_path = cls.get_main_path()
        ScoutCampException.set_error_log(ErrorLog(cls.program_path, 'camp'))

        # Criar novo projeto
        if mode == "init":
            cls.init(project_name)

        # Checagem para obter as configurações
        cls.progress('config_c')
        if conf_override:
            cls.configs = Config(conf_override)
        else:
            cls.configs = Config()

        # Iniciar servidor
        if mode == "server":
            cls.server()


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

        cls.progress('temp_c')
        cls.instance_templates()

        cls.progress('local_c')
        cls.instance_localization()

        cls.progress('assets_c')
        cls.copy_assets()

        cls.dump_variables()

        cls.progress('comp_page')
        cls.render_templates()



    @classmethod
    def instance_templates(cls):
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



    @classmethod
    def instance_localization(cls):
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



    @classmethod
    def copy_assets(cls):

        try:
            shutil.copy('favicon.ico', cls.configs.get_path_to('index')+"favicon.ico")
        except IOError:
            printc(" > Favicon não encontrado <", 'yellow')

        copy_tree(
            cls.configs.get_path_to('assets'),
            cls.configs.get_path_to('index')+cls.configs.get_build_path_to('assets')
        )



    @classmethod
    def dump_variables(cls):

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

            # check if dump json
            json_parser.save_all(badge_base, cls.configs.get_variable(term), cls.configs.get_build_path_to("data"))

        cls.data_base[cls.configs.get_variable("custom")] = cls.configs.get_custom_variables()
        # check if dump json
        json_parser.save(json_parser.to_json(cls.configs.get_custom_variables(), 4), cls.configs.get_variable("custom"), cls.configs.get_build_path_to("data"))



    @classmethod
    def render_templates(cls):

        ignore_escape = lambda do_nothing: do_nothing

        temp_maker = pystache.Renderer(string_encoding='utf8', escape=ignore_escape)

        template_dict = dict()
        template_dict.update({"camp":cls.configs.get_camp()})
        template_dict.update(cls.main_language.get_terms())
        template_dict.update(cls.data_base)

        rendered_board = jinjo.Template(
            cls.main_scoutboard("string")).render(
            template_dict
        )

        template_dict.update({"table":rendered_board})

        rendered_html = jinjo.Template(
            cls.main_template("string")).render(
            template_dict
        )

        html_output = open(cls.configs.get_path_to("index") + "index.html","w", encoding='utf-8')
        html_output.write(rendered_html)
        html_output.close()

        for i in range(len(cls.script_template.get_templates())):
            rendered_script = jinjo.Template(
                cls.script_template.get_templates()[i]).render(
                template_dict
            )
            js_output = open(
                cls.configs.get_path_to("index")+cls.configs.get_build_path_to("scripts")+cls.script_template.get_template_list()[i]+".js",
                "w", encoding='utf-8'
            )
            js_output.write(rendered_script)
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
        printc("\n -*- Penso, logo mito -*-", "magenta")
        sys.exit()


    @staticmethod
    def get_main_path():
        path = os.path.dirname(sys.argv[0])
        if len(path) > 0:
            path += '/'
        return path


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
            'assets_c': " Copiando assets...",
            'comp_term': " Compilando "+term+"...",
            'comp_page': " Compilando páginas...",
            'download_temp': " Baixando templates...",
            'unzip': " Extraindo templates...",
            'unziped': paint(" Projeto criado!", 'green'),
            'comp_end': paint(" Compilação finalizada!", 'green')
        }
        prints(messages_unicode[prog])


    @classmethod
    def init(cls, project_name):
        if not os.path.isdir(project_name):
            from zipfile import ZipFile

            if not os.path.isfile(cls.program_path+'base_project.zip'):
                try:
                    cls.progress('download_temp')
                    TemplateUpdate.download_template()
                except Exception as e:
                    ServerException(" Não foi possível baixar o template, verifique sua conexão e tente novamente!", e)
                    raise
                    sys.exit(1)

            try:
                if TemplateUpdate.has_update():
                    printc("Há uma nova versão do template disponível!", 'yellow')
                    prints("Deseja baixar? (Y/N)")

                    update = None
                    while update != "Y" and update != "N":
                        update = raw_input('> ').upper()
                        if update == "Y":
                            TemplateUpdate.download_template()
            except Exception as e:
                printc(" Não foi possível checar a versão do template, usando o template atual...", 'yellow')


            cls.progress('unzip')
            template_file = cls.program_path+'base_project.zip'

            with ZipFile(template_file, "r") as init_zip:
                init_zip.extractall("")

            os.rename('scout-camp-template-master', project_name)

        else:
            printc(" A pasta {} já existe!".format(project_name), 'yellow')
            sys.exit(1)

        cls.progress("unziped")
        sys.exit(0)



if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(prog="ScoutCamp", description="Scout Camp - Static HTML Group Manager")
    parser.add_argument("-r","--render", help="compile project using default config file", action="store_true")
    parser.add_argument("-p","--path", metavar="alternative-path", help="compile using alternative path")
    parser.add_argument("-c","--create", metavar="project-name", help="create new ScoutCamp project")
    parser.add_argument("-t","--test", metavar="config-file", help="compile using another config file")
    parser.add_argument("-s","--server", help="start the Scout Camp server", action="store_true")
    parser.add_argument("-d","--data", help="generate SQLite database [experimental]", action="store_true")
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
            printc(" Use o comando --path com --render ou --server!", 'yellow')

    elif args.test:
        if args.server:
            ScoutCamp.main(conf_override=args.test, mode="server")
        elif args.render:
            ScoutCamp.main(conf_override=args.test)
        else:
            printc(" Use o comando --test com --render ou --server!", 'yellow')

    elif args.server:
        ScoutCamp.main(mode="server")

    elif args.version:
        printc(ScoutCamp.get_full_version(), 'cyan')

    elif args.create:
        prints(ScoutCamp.main(mode="init", project_name=args.create))

    elif args.render:
        ScoutCamp.main()

    else:
        printc(ScoutCamp.get_full_version(), 'cyan')
        parser.print_help()
