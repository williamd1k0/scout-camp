# -*- encoding: utf-8 -*-

import sys
import errno
import webbrowser
import SocketServer
import SimpleHTTPServer
from utils import Utils
from socket import error as socket_error

printc = Utils.printc
prints = Utils.prints


class Server(object):

    __port = None
    __host = None
    __open_browser = None
    __httpd = None

    def __init__(self, _host=None, _port=None, _open_browser=None):

        if _host is not None:
            self.__host = _host
        else:
            self.__host = "localhost"

        if _port is not None:
            self.__port = _port
        else:
            self.__port = 80

        if _open_browser is not None:
            self.__open_browser = _open_browser
        else:
            self.__open_browser = True

        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        try:
            self.__httpd = SocketServer.TCPServer((self.__host, self.__port), Handler)
        except socket_error as serr:
            if serr.errno == errno.WSAEACCES:
                printc(" Não foi possível criar o servidor, a porta {} pode estar sendo usada!".format(self.__port),'red')
            else:
                raise serr
            exit(1)



    def start_server(self, _auto_exec=None):

        if _auto_exec is None:
            _auto_exec = self.__open_browser

        if _auto_exec:
            self.open_browser()

        self.server_message('on')
        try:
            self.__httpd.serve_forever()
        except:
            pass

        self.__httpd.server_close()
        self.server_message('off')


    def server_message(self, _mode):
        if _mode == "on":
            prints("\n> ScoutCamp serving at port {}".format(self.__port))
            prints("> Open your browser and go to http://{}/".format(self.__host))
            prints("\n> Press Ctrl+C or close window to shut down the server\n")
        elif _mode == 'off':
            prints(" Servidor desativado")


    def open_browser(self):
        webbrowser.open("http://{}:{}".format(self.__host, self.__port))


if __name__ == '__main__':
    camp = Server()
    camp.start_server()
