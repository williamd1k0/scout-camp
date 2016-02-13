# -*- encoding: utf-8 -*-


class Utils(object):


    @staticmethod
    def prints(string):
        try:
            print(unicode(string, 'utf8'))
        except:
            print(string)
