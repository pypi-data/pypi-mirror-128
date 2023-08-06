#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/2 14:46
# @Author  : Adyan
# @File    : Rabbit_conn.py


import json
import pika

from zhanlan_pkg.Utils import rabitmq_config


class RabbitClient:
    def __init__(self, queue_name):
        self.queue_name = queue_name

    def rabbit_conn(self):
        """
        创建连接
        :return:
        """
        user_pwd = pika.PlainCredentials(
            rabitmq_config.get("mq_username"),
            rabitmq_config.get("mq_pwd")
        )
        params = pika.ConnectionParameters(
            host=rabitmq_config.get("mq_ip"),
            port=rabitmq_config.get('mq_port'),
            virtual_host=rabitmq_config.get("mq_virtual_host"),
            credentials=user_pwd
        )
        self.conn = pika.BlockingConnection(parameters=params)
        self.col = self.conn.channel()
        self.col.queue_declare(
            queue=self.queue_name,
            durable=True
        )

    def push_rabbit(self, item):
        self.rabbit_conn()
        self.col.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(item, ensure_ascii=False)
        )

    def get_rabbit(self, fun):
        self.rabbit_conn()
        self.col.queue_declare(self.queue_name, durable=True, passive=True)
        self.col.basic_consume(self.queue_name, fun)
        self.col.start_consuming()


if __name__ == '__main__':
    # # 一键搬家
    # RabbitClient('TEST_SMT_COPY_PRODUCT').push_rabbit(
    #     {"request_type": "SMT_COPY_PRODUCT", "request_id": "2cac500ba49c4fb97d9a80eb3f9cb216",
    #      "secret_key": "_QXSYYXGJQUQS", "biz_id": "https:\\/\\/detail.1688.com\\/offer\\/614651326996.html",
    #      "send_at": 1629164414,
    #      "data": {"productUrl": "https:\\/\\/detail.1688.com\\/offer\\/614651326996.html", "type": 1}}
    # )
    # 查排名
    RabbitClient('TEST_SMT_PRODUCT_RANKING').push_rabbit(
        {"send_at": 1619520635,
         "data": {"keyword": "衣服", "shopName": "东莞市汇百商网络科技有限公司", "shopUrl": "shop085o885b77228.1688.com",
                  "productUrl": "", "type": "3", "startPage": "1", "endPage": "3", "requestId": 8703}}

    )
