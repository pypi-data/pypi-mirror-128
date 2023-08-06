# -*- coding = UTF-8 -*-
# Author   : buxiubuzhi
# Project  : lazyTest
# FileName : page.py
# Describe :
# ---------------------------------------

import logging
import warnings

import lazyTest


class Page(object):
    __configFile = "\\pytest.ini"

    __section = "pytest"

    def __init__(self, driver: lazyTest.WebOption):
        self.driver = driver
        self.lazyLog = logging.getLogger(self.getClassName())
        self.config = lazyTest.ReadIni(self.GetProjectPath() + self.__configFile)
        path = self.GetProjectPath() + self.__getFilePath() + self.getClassName() + self.__getSuffix()
        self.lazyLog.info("元素文件: -> %s" % path)
        data = lazyTest.ReadYaml(path)
        self.source = lazyTest.ElementSource(**data)

    def __getFilePath(self):
        return self.config.GetIniConfig(self.__section, "elementPath")

    def __getSuffix(self):
        return self.config.GetIniConfig(self.__section, "suffix")

    def GetElement(self, key: str):
        warnings.warn("请使用新的获取方式:Element",DeprecationWarning)
        return self.source.GetEle(key)

    def Element(self,key: str):
        return self.source.GetEle(key)

    def GetProjectPath(self) -> str: ...

    @classmethod
    def getClassName(cls):
        return cls.__name__
