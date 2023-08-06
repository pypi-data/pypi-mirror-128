#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/26 14:20
# @Author  : Adyan
# @File    : __init__.py.py

from .Rabbit_conn import *
from .Redis_conn import *
from .monitor_rabbit import *
from .MyUtils import *
from .Mongo_conn import *
from .proxy import *

root_config = {
    "SPIDER": {
        "log_dir_path": "./log"
    },
    "MYSQL": {
        "HOST": "119.29.9.92",
        "PORT": 3306,
        "USER": "root",
        "PASSWD": "zl123456",
        "DBNAME": "taobao"
    },
    "MONGO": {
        "host": "192.168.20.211",
        # "host": "119.29.9.92",
        # "host": "47.107.86.234",
        "port": 27017
    },
    "REDIS": {
        "HOST": "119.29.9.92",
        # "HOST":"47.107.86.234",
        "PORT": 6379,
        "DB": 11
    },
    "TASK_REDIS": {
        "HOST": "119.29.9.92",
        "PORT": 6379,
    },
    "OPERATE_CONFIG": {
        "GET_SHOPS_URL": "http://localhost:8000/getAllShop",
        "SAVE_DATA_URL": "http://119.29.9.92/crm/saveCrmData",
        "GET_GOOD_COOKIE_URL": "http://localhost:8000/getRandomCookie",
        "DEL_COOKIE_URL": "http://localhost:8000/delExpiredCookie?id="
    },
    "MACHINE_CONFIG": {
        "MACHINE_NO": 0
    },
    "AUTO_LOGIN_CONFIG": {
        "IP": "http://localhost:8000"
    },
    "PROXY_KEY": ["shop_list"],
    "SYNC_CONFIG": {
        "shop_list": 0
    },
    "ZL_CONFIG": {
        "OFFICIAL_IP": "http://localhost:8000"
    },
    "RABITMQ_CONFIG": {
        "mq_ip": "121.89.219.152",
        "mq_port": 30002,
        "mq_virtual_host": "my_vhost",
        "mq_username": "dev",
        "mq_pwd": "zl123456",
        "prefix": ""
        # "prefix": "TEST_"
    },
    "GOOD_COUNT_IP": {
        'server': "https://erp.zlkj.com/"
    },
    "MOGU_PROXY": {
        "proxyServer": "secondtransfer.moguproxy.com:9001",
        "proxyAuth": "Basic d25ZU3YxekxZSk40Y3hydDozN01uN0lLTFViZkdUY2tK"

    }

}

# browser_config = root_config.get("BROWSER", {})
redis_config = root_config.get("REDIS", {})
mysql_config = root_config.get("MYSQL", {})
spider_config = root_config.get('SPIDER', {})
mongo_config = root_config.get('MONGO', {})
auto_login_config = root_config.get("AUTO_LOGIN_CONFIG")
dm_config = root_config.get("ZL_CONFIG", {})
task_redis_config = root_config.get("TASK_REDIS")
celery_redis_config = root_config.get("REDIS")
proxy_key_list = root_config.get("PROXY_KEY")
operate_config = root_config.get("OPERATE_CONFIG")
machine_config = root_config.get("MACHINE_CONFIG", {})
sync_config = root_config.get("SYNC_CONFIG", {})
rabitmq_config = root_config.get("RABITMQ_CONFIG", {})
# post_data_config = root_config.get("POSTDATAURL", {})
good_count_server = root_config.get("GOOD_COUNT_IP", {})
mogu_config = root_config.get("MOGU_PROXY", {})
