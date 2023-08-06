# -*- coding: utf-8 -*-
"""
@Time    : 2021/11/22 13:41
@Author  : lrabbit
@FileName: spider.py
@Software: PyCharm
@Blog    : https://www.lrabbit.life
"""


class Excepiton403(Exception):
    def __init__(self):
        self.__name = "exception403"


class Excepiton404(Exception):
    def __init__(self):
        self.__name = "exception404"


class Excepiton500(Exception):
    def __init__(self):
        self.__name = "exception500"


if __name__ == '__main__':
    print(type(Excepiton403()).__name__)
