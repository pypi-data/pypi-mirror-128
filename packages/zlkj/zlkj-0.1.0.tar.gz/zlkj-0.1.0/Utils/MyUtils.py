#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/29 19:09
# @Author  : Adyan
# @File    : MyUtils.py

import json
import re
import time
import pytz
import random

from datetime import datetime
from faker import Faker

from zhanlan_pkg.Utils.Mongo_conn import MongoPerson

fake = Faker()
cntz = pytz.timezone("Asia/Shanghai")


class ReDict:

    @classmethod
    def string(
            cls,
            re_pattern: dict,
            string_: str,
    ):
        if string_:
            return {
                key: cls.compute_res(
                    re_pattern=re.compile(scale),
                    string_=string_.translate(
                        {
                            ord('\t'): '', ord('\f'): '',
                            ord('\r'): '', ord('\n'): '',
                            ord(' '): '',
                        })
                )
                for key, scale in re_pattern.items()
            }

    @classmethod
    def compute_res(
            cls,
            re_pattern: re,
            string_=None
    ):
        data = [
            result.groups()[0]
            for result in re_pattern.finditer(string_)
        ]
        if data:
            try:
                return json.loads(data[0])
            except:
                return data[0]
        else:
            return None


class Utils:

    @classmethod
    def time_cycle(
            cls,
            times,
            int_time=None
    ):
        """
        入库时间规整
        :param times: string - 字符串时间
        :param int_time: True and False  - 获时间戳
        :return:
        """
        if int_time:
            return int(time.mktime(time.strptime(times, "%Y-%m-%d")))
        if type(times) is str:
            times = int(time.mktime(time.strptime(times, "%Y-%m-%d %H:%M:%S")))
        return str(datetime.fromtimestamp(times, tz=cntz))

    @classmethod
    def merge_dic(
            cls,
            dic: dict,
            lst: list
    ):
        """
        合并多个dict
        :param dic: dict - 主dict
        :param lst: list - 多个字典列表方式传入
        :return:
        """
        for d in lst:
            for k, v in d.items():
                if v:
                    dic[k] = v
        return dic

    @classmethod
    def is_None(
            cls,
            dic: dict,
    ) -> dict:
        """
        :param dic: dict
        :return: 返回字典中值是None的键值对
        """
        return {
            k: v
            for k, v in dic.items()
            if not v
        }

    @classmethod
    def find(
            cls, target: str,
            dictData: dict,
    ) -> list:
        queue = [dictData]
        result = []
        while len(queue) > 0:
            data = queue.pop()
            for key, value in data.items():
                if key == target:
                    result.append(value)
                elif isinstance(value, dict):
                    queue.append(value)
        if result:
            return result[0]


class Headers:

    def headers(self, referer=None):
        while True:
            user_agent = fake.chrome(
                version_from=63, version_to=80, build_from=999, build_to=3500
            )
            if "Android" in user_agent or "CriOS" in user_agent:
                continue
            else:
                break
        if referer:
            return {
                "user-agent": user_agent,
                "referer": referer,
            }
        return {
            "user-agent": user_agent,
        }


class Cookies(object):

    def __init__(self, db_name):
        self.mongo_conn = MongoPerson(db_name, 'cookie').test()

    def cookie(self):
        return random.choice(list(self.mongo_conn.find()))
