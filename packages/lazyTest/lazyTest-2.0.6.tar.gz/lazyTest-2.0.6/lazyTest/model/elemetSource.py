# -*- coding = UTF-8 -*-
# Author   : xingHeYang
# time     : 2021/11/8 21:08
# ---------------------------------------


class ElementSource:
    __page = "page"
    __ele = "ele"

    def __init__(self, **kwargs):
        self.source = kwargs

    def __getPage(self):
        return self.source[self.__page]

    def __getKey(self, key):
        return self.__getPage()[key]

    def GetEle(self, key):
        return self.__getKey(key)[self.__ele]

    def GetKey(self, key):
        return self.source[key]
