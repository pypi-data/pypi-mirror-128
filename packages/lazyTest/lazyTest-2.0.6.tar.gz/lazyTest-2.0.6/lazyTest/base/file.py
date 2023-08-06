# -*- coding = UTF-8 -*-
# Author   : buxiubuzhi
# Project  : lazyTest
# FileName : file.py
# Describe :
# ---------------------------------------
import configparser
from typing import List
import csv
from ruamel import yaml


def ReadYaml(path: str):
    """读取yaml文件"""
    with open(path, 'r', encoding='UTF-8') as fp:
        yaml_data = yaml.safe_load(fp)
    return yaml_data


class ReadIni:

    def __init__(self, path):
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def GetIniConfig(self, section, key):
        """读取ini文件"""
        return self.config.get(section, key)


def ReadCsvFileToList(filePath):
    """读取CSV文件,参数化使用"""
    with open(filePath, 'r', encoding='utf8') as fp:
        data_list = [i for i in csv.reader(fp)]
    if len(data_list[0]) == 1:
        data_list.pop(0)  # 去首行
        return [i[0] for i in data_list]
    else:
        data_list.pop(0)  # 去首行

    return data_list
