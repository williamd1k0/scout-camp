import SimpleHTTPServer
import SocketServer
import webbrowser

class Server:

    __port = 80
    __host = "localhost"

    def __init__(self, host=None, port=None):

        if port:
            self.__port = port
        if host:
            self.__host = host

        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        self.httpd = SocketServer.TCPServer((self.__host, self.__port), Handler)


    def infinite(self, auto_exec=True):

        if auto_exec:
            self.open_chrome()

        self.server_message()
        try:
            self.httpd.serve_forever()
        except:
            pass

        self.httpd.server_close()
        print " Server switched off, press Enter to exit"
        raw_input()

    def server_message(self):

        print "\n> Scout Camp serving at port {}".format(self.__port)
        print "> Open your browser and go to http://{}/".format(self.__host)
        print "\n> Press Ctrl+C or close window to shut down the server\n"


    def open_chrome(self):

        webbrowser.open("http://{}".format(self.__host))


if __name__ == '__main__':

    camp = Server()
    camp.infinite()
