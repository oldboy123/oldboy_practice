#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
print(os.path.abspath(__file__))

import getpass
#import re

"""By xuzhigui"""

f = open('db', 'rU')
users_info = f.read()
temp_users_infos = users_info.split('\n')

i = 0
users_info_list = []
while i < len(temp_users_infos):
    user_value = temp_users_infos[i]
    if len(temp_users_infos[i].strip()) > 0:
        users_info_list.append(user_value)
    i += 1


# users_info_list = [i for i in temp_users_infos if i]


# 调试输出用户信息
print(users_info_list)

users_info_dict = {}

for user_info in users_info_list:
    user_pwd_time = []
    uname = user_info.split("|")[0]
    pwd = user_info.split('|')[1]
    times = user_info.split('|')[2]
    user_pwd_time.append(pwd)
    user_pwd_time.append(times)

    temp_dict = {uname: user_pwd_time}
    users_info_dict.update(temp_dict)


over_while = True

# {"alex":[pass, 'times'], "eric":["pass", 'times'] }

while over_while:
    username = input("请输入用户名信息:")

    if username in users_info_dict.keys():
        user_info = users_info_dict[username]
        pwd = users_info_dict[username][0]
        times = users_info_dict[username][1]
        if int(times) != 0:
            password = input("请输入密码:")
            if password == pwd:
                print("登录成功，欢迎！")
                users_info_dict[username][1] = '3'
                over_while = False
                break
            else:
                print("输入信息错误，请输入正确的用户名和密码")
                users_info_dict[username][1] = str(int(users_info_dict[username][1]) - 1)
                if int(users_info_dict[username][1]) == 0:
                    #跳出while循环
                    over_while = False
                    break
        else:
            print("已超过登录次数限制，账户被锁定")
            over_while = False
            break


# TODO 写会用户信息到文件

print(users_info_dict)
'eric|456|3'

f = open('db', 'w')
f.truncate()
f.close()

for k,v in users_info_dict.items():
    content = "%s|%s|%s\n" % (k, v[0], v[1])
    f = open('db', 'a+')
    f.write(content)
    f.close()