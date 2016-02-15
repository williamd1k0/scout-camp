# -*- encoding: utf-8 -*-

from colorama import Fore, init


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
    def prints(_string):
        try:
            print(unicode(_string, 'utf8'))
        except:
            print(_string)


    @classmethod
    def printc(cls, _string, _color):
        cls.prints(cls.paint(_string, _color))


    @classmethod
    def paint(cls, _string, _color):
        return cls.__COLORS[_color] + _string + cls.__COLORS["default"]



if __name__ == '__main__':
    pass
