#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys,os
import hashlib
from conf import settings

class User_operation():
    '''对登录信息进行认证，登录成功返回用户名，失败返回None'''
    def authentication(self,login_info):
        list = login_info.split(":")            #对信息进行分割
        login_name = list[0]
        login_passwd = self.hash(list[1])
        DB_FILE = settings.DATABASE + r"\%s.db"%login_name
        if os.path.isfile(DB_FILE):
            user_database = self.cat_database(DB_FILE)  #用户数据库信息
            if login_name == user_database["username"]:
                if login_passwd == user_database["password"]:
                    return user_database

    def cat_database(self,DB_FILE):
        #获取数据库信息
        with open(DB_FILE,"r") as file:
            data = json.loads(file.read())
            return  data

    def hash(self,passwd):
        '''对密码进行md5加密'''
        m = hashlib.md5()
        m.update(passwd.encode("utf-8"))
        return m.hexdigest()
