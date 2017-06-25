#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socketserver
import sys,os
import hashlib
from os.path import join, getsize
from conf import settings
from modules import auth_user


class Myserver(socketserver.BaseRequestHandler):
    '''ftp服务端'''
    def handle(self):
        try:
            self.conn = self.request
            while True:
                login_info = self.conn.recv(1024).decode()    # 接收客户端发的的账号密码信息
                result = self.authenticat(login_info)
                status_code = result[0]
                self.conn.sendall(status_code.encode())
                if status_code == "400":
                    continue
                self.user_db = result[1]             #当前登录用户信息
                self.current_path = self.user_db["homepath"]    #用户当前目录
                self.home_path = self.user_db["homepath"]  #用户宿主目录

                while True:
                    command = self.conn.recv(1024).decode()
                    command_str = command.split()[0]
                    if hasattr(self,command_str):
                        func = getattr(self,command_str)
                        func(command)
                    else:self.conn.sendall("401".encode())
        except ConnectionResetError as e:
            self.conn.close()
            print(e)

    def authenticat(self,login_info):
        '''认证用户'''
        auth = auth_user.User_operation()       # 创建认证实例
        result = auth.authentication(login_info)         # 认证用户
        if result:return "200",result
        else:return "400",result

    def get(self,command):
        '''下载文件'''
        if len(command.split()) > 1:
            filename = command.split()[1]
            file_path = self.current_path + r"\%s"%filename
            if os.path.isfile(file_path):               #文件是否存在
                self.conn.sendall("201".encode())      #命令可执行
                file_size = os.stat(file_path).st_size  # 文件总大小
                status_code = self.conn.recv(1024).decode()

                # 客户端存在此文件
                if status_code == "403":
                    self.conn.sendall("000".encode())   #系统交互
                    has_send_size = self.conn.recv(1024).decode()
                    has_send_size = int(has_send_size)
                    # 客户端文件不完整可续传
                    if has_send_size < file_size:
                        self.conn.sendall("205".encode())
                        file_size -= has_send_size  #续传文件大小
                        response = self.conn.recv(1024)  # 等待响应

                    # 客户端文件完整不可续传、不提供下载
                    else:
                        self.conn.sendall("405".encode())
                        return
                # 客户端不存在此文件
                elif status_code == "402":
                    has_send_size = 0

                with open(file_path,"rb") as file:
                    self.conn.sendall(str(file_size).encode())       #发送文件大小
                    response = self.conn.recv(1024)     #等待响应
                    file.seek(has_send_size)
                    m = hashlib.md5()
                    for line in file:
                        m.update(line)
                        self.conn.sendall(line)
                self.conn.sendall(m.hexdigest().encode())     #发送文件md5值
            else:self.conn.sendall("402".encode())
        else:self.conn.sendall("401".encode())

    def put(self,command):
        '''上传文件'''
        filename = command.split()[1]
        file_path = self.current_path + r"\%s" % filename
        self.conn.sendall("000".encode())   #发送确认
        file_size = self.conn.recv(1024).decode()  # 文件大小
        file_size = int(file_size)
        limit_size = self.user_db["limitsize"]      #磁盘额度
        used_size = self.__getdirsize(self.home_path)   #已用空间大小
        if limit_size >= file_size+used_size:
            self.conn.sendall("202".encode())
            with open(file_path, "wb") as file:  # 开始接收
                revice_size = 0
                m = hashlib.md5()
                while revice_size < file_size:
                    minus_size = file_size - revice_size
                    if minus_size > 1024:
                        size = 1024
                    else:
                        size = minus_size
                    data = self.conn.recv(size)
                    revice_size += len(data)
                    file.write(data)
                    m.update(data)
                new_file_md5 = m.hexdigest()  # 生成新文件的md5值
                server_file_md5 = self.conn.recv(1024).decode()
                if new_file_md5 == server_file_md5:  # md5值一致
                    self.conn.sendall("203".encode())
        else:self.conn.sendall("404".encode())


    def dir(self,command):
        '''查看当前目录下的文件'''
        if len(command.split()) == 1:
            self.conn.sendall("201".encode())
            response = self.conn.recv(1024)
            send_data = os.popen("dir %s"%self.current_path)
            self.conn.sendall(send_data.read().encode())
        else:self.conn.sendall("401".encode())

    def pwd(self,command):
        '''查看当前用户路径'''
        if len(command.split()) == 1:
            self.conn.sendall("201".encode())
            response = self.conn.recv(1024)
            send_data = self.current_path
            self.conn.sendall(send_data.encode())
        else:self.conn.sendall("401".encode())

    def mkdir(self,command):
        '''创建目录'''
        if len(command.split()) > 1:
            dir_name = command.split()[1]       #目录名
            dir_path = self.current_path + r"\%s"%dir_name #目录路径
            if not os.path.isdir(dir_path):     #目录不存在
                self.conn.sendall("201".encode())
                response = self.conn.recv(1024)
                os.popen("mkdir %s"%dir_path)
            else:self.conn.sendall("403".encode())
        else:self.conn.sendall("401".encode())

    def cd(self,command):
        '''切换目录'''
        if len(command.split()) > 1:
            dir_name = command.split()[1]       #目录名
            dir_path = self.current_path + r"\%s" %dir_name    #目录路径
            user_home_path = settings.HOME_PATH + r"\%s"%self.user_db["username"]   #宿主目录
            if dir_name == ".." and len(self.current_path)>len(user_home_path):
                self.conn.sendall("201".encode())
                response = self.conn.recv(1024)
                self.current_path = os.path.dirname(self.current_path)  #返回上一级目录
            elif  os.path.isdir(dir_path)   :
                self.conn.sendall("201".encode())
                response = self.conn.recv(1024)
                if dir_name != "." and dir_name != "..":
                    self.current_path += r"\%s"%dir_name        #切换目录

            else:self.conn.sendall("402".encode())
        else:self.conn.sendall("401".encode())

    def __getdirsize(self,home_path):
        '''统计目录空间大小'''
        size = 0
        for root, dirs, files in os.walk(home_path):
            size += sum([getsize(join(root, name)) for name in files])
        return size

