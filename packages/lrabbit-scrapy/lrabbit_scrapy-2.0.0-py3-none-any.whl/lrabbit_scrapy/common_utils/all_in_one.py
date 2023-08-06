# -*- coding: utf-8 -*-
"""
@Time    : 2021/11/18 10:22
@Author  : lrabbit
@FileName: all_in_one.py
@Software: PyCharm
@Blog    : https://www.lrabbit.life
"""

"""

this module you can find any you usually used function

"""
import datetime


def get_time_format_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
