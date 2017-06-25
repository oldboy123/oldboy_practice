#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os,hashlib
import json
from conf import settings
from modules import auth_user
from modules import sokect_server


def create_db():
    '''创建用户数据库文件'''
    user_database={}
    encryption = auth_user.User_operation()
    limitsize = settings.LIMIT_SIZE
    for k,v in settings.USERS_PWD.items():
        username = k
        password = encryption.hash(v)
        user_db_path  = settings.DATABASE + r"\%s.db"%username
        user_home_path = settings.HOME_PATH + r"\%s"%username
        user_database["username"] = username
        user_database["password"] = password
        user_database["limitsize"] = limitsize
        user_database["homepath"] = user_home_path
        if not os.path.isfile(user_db_path):
            with open(user_db_path,"w") as file:
                file.write(json.dumps(user_database))

def create_dir():
    '''创建用户属主目录'''
    for username in settings.USERS_PWD:
        user_home_path = settings.HOME_PATH + r"\%s" %username
        if not os.path.isdir(user_home_path):
            os.popen("mkdir %s" %user_home_path)



if __name__ == "__main__":
    '''初始化系统数据并启动程序'''
    create_db()         #创建数据库
    create_dir()        #创建属主目录
                        #启动ftp服务
    server = sokect_server.socketserver.ThreadingTCPServer(settings.IP_PORT, sokect_server.Myserver)
    server.serve_forever()
