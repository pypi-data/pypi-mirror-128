#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/2 17:43
# @Author  : Adyan
# @File    : Redis_conn.py


import redis

from datetime import datetime

from zhanlan_pkg.Utils import redis_config

HOST = redis_config.get('HOST', 'localhost')
PORT = redis_config.get('PORT', 6379)
PASSWORD = redis_config.get('PAW', None)
DB = redis_config.get('DB', 0)


class ReidsClient(object):

    def __init__(self, host=HOST, port=PORT, password=PASSWORD, db=None, NAME=None):
        if db == None:
            db = DB
        if password:
            self.__conn = redis.Redis(host=host, port=port, password=password)
        else:
            self.__conn = redis.Redis(host=host, port=port, db=db)
        self.NAME = NAME

    def redis_conn(self):
        return self.__conn

    def get(self, count):
        lst = self.__conn.lrange(self.NAME, 0, count - 1)
        self.__conn.ltrim(self.NAME, count, -1)
        return lst

    def put(self, param):
        self.__conn.rpush(self.NAME, param)

    @property
    def queue_len(self):
        return self.__conn.llen(self.NAME)

    def prox(self):
        ip_list = []
        data_list = self.__conn.hgetall("proxy")
        for ip_item in data_list:
            proxy_expire_time = int(data_list[ip_item].decode())
            now_time = int(datetime.now().timestamp())
            time_dif = proxy_expire_time - now_time
            if time_dif < 10:
                print(ip_item.decode(), "过期 删除这个代理")
                self.__conn.hdel('proxy', ip_item)
            else:
                ip_list.append(ip_item.decode())
        return ip_list
