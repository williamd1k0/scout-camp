import SimpleHTTPServer
import SocketServer
import webbrowser

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
        self.__httpd = SocketServer.TCPServer((self.__host, self.__port), Handler)


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
            print("\n> ScoutCamp serving at port {}".format(self.__port))
            print("> Open your browser and go to http://{}/".format(self.__host))
            print("\n> Press Ctrl+C or close window to shut down the server\n")
        elif _mode == 'off':
            print(" Servidor desativado")


    def open_browser(self):
        webbrowser.open("http://{}:{}".format(self.__host, self.__port))


if __name__ == '__main__':
    camp = Server()
    camp.start_server()
