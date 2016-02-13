# -*- encoding: utf-8 -*-


class Utils(object):

    __COLORS = {
        "pink":'\033[95m',
        "blue":'\033[94m',
        "green":'\033[92m',
        "yellow":'\033[93m',
        "red":'\033[91m',
        "default":'\033[0m',
        "white":'\033[1m',
        "underline":'\033[4m'
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