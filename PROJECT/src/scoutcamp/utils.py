# -*- encoding: utf-8 -*-

from colorama import Fore, init
import os.path


class Utils(object):

    __COLORS = {
        "magenta": Fore.MAGENTA,
        "blue": Fore.BLUE,
        "cyan": Fore.CYAN,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "red": Fore.RED,
        "black": Fore.BLACK,
        "white": Fore.WHITE,
        "default": Fore.RESET
    }


    @staticmethod
    def prints(string_):
        try:
            print(unicode(string_, 'utf8'))
        except:
            print(string_)


    @classmethod
    def printc(cls, string_, color_):
        cls.prints(cls.paint(string_, color_))


    @classmethod
    def paint(cls, string_, color_):
        return cls.__COLORS[color_] + string_ + cls.__COLORS["default"]
    
    
    @classmethod
    def recursive_mkdir(cls, path, start=''):
        if os.path.isdir(os.path.join(start, path)): return False
        import re as regxp
        paths = regxp.sub('[\\\/]+', r'\\', path).split('\\')
        paths_i = [start]
        for folder in paths:
            paths_i.append(folder)
            absolute = '\\'.join(paths_i)
            if not os.path.isdir(absolute):
                os.mkdir(absolute)
        del regxp


class ErrorLog(object):

    __path = None
    __name = None
    __ext = None

    def __init__(self, _path='', _name='', _ext='.log'):
        self.__path = _path
        self.__name = _name
        self.__ext = _ext


    def log(self, info):
        log_string = '\n\n---------------> [ YYY-MM-DD | hh:mm ]\n'
        log_string += str(info)
        log = open(self.get_logfile(), 'w')
        log.write(log_string)
        log.close()


    def get_logfile(self):
        return self.__path+self.__name+self.__ext


    def get_datetime(self):
        pass



if __name__ == '__main__':
    pass
