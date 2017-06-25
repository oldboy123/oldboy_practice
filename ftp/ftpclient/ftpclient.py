#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import os,sys
import hashlib

class Myclient():
    '''ftp客户端'''
    def __init__(self,ip_port):
        self.ip_port = ip_port

    def connect(self):
        '''连接服务器'''
        self.client = socket.socket()
        self.client.connect(self.ip_port)

    def start(self):
        '''程序开始'''
        self.connect()
        while True:
            username = input("输入用户名：").strip()
            password = input("输入密码：").strip()
            login_info = ("%s:%s" %(username, password))
            self.client.sendall(login_info.encode())        #发送用户密码信息
            status_code = self.client.recv(1024).decode()   #返回状态码
            if status_code == "400":
                print("[%s]用户密码认证错误"%status_code)
                continue
            else:print("[%s]用户密码认证成功"%status_code)
            self.interactive()

    def interactive(self):
        '''开始交互'''
        while True:
            command = input("->>").strip()
            if not command:continue
            #if command == "exit":break
            command_str = command.split()[0]
            if hasattr(self,command_str):           # 执行命令
                func = getattr(self,command_str)
                func(command)
            else:print("[%s]命令不存在"%401)

    def get(self,command):
        '''下载文件'''
        self.client.sendall(command.encode())  #发送要执行的命令
        status_code = self.client.recv(1024).decode()
        if status_code == "201":            #命令可执行
            filename = command.split()[1]

            # 文件名存在，判断是否续传
            if os.path.isfile(filename):
                revice_size = os.stat(filename).st_size     #文件已接收大小
                self.client.sendall("403".encode())
                response = self.client.recv(1024)
                self.client.sendall(str(revice_size).encode())   #发送已接收文件大小
                status_code = self.client.recv(1024).decode()

                # 文件大小不一致，续传
                if status_code == "205":
                    print("继续上次上传位置进行续传")
                    self.client.sendall("000".encode())

                # 文件大小一致，不续传,不下载
                elif status_code == "405":
                    print("文件已经存在，大小一致")
                    return

            # 文件不存在
            else:
                self.client.sendall("402".encode())
                revice_size = 0

            file_size = self.client.recv(1024).decode() #文件大小
            file_size = int(file_size)
            self.client.sendall("000".encode())

            with open(filename,"ab") as file:      #开始接收
                #file_size 为文件总大小
                file_size +=revice_size
                m = hashlib.md5()
                while revice_size < file_size:
                    minus_size = file_size - revice_size
                    if minus_size > 1024:
                        size = 1024
                    else:
                        size = minus_size
                    data = self.client.recv(size)
                    revice_size += len(data)
                    file.write(data)
                    m.update(data)
                    self.__progress(revice_size,file_size,"下载中")      #进度条
                new_file_md5 = m.hexdigest()        #生成新文件的md5值
                server_file_md5 = self.client.recv(1024).decode()
                if new_file_md5 == server_file_md5:     #md5值一致
                    print("\n文件具有一致性")
        else:print("[%s] Error！"%(status_code))

    def put(self,command):
        '''上传文件'''
        if len(command.split()) > 1:
            filename = command.split()[1]
            #file_path = self.current_path + r"\%s"%filename
            if os.path.isfile(filename):               #文件是否存在
                self.client.sendall(command.encode())  #发送要执行的命令
                response = self.client.recv(1024)      #收到ack确认

                file_size = os.stat(filename).st_size  # 文件大小
                self.client.sendall(str(file_size).encode())  # 发送文件大小
                status_code = self.client.recv(1024).decode()  # 等待响应,返回状态码
                if status_code == "202":
                    with open(filename,"rb") as file:
                        m = hashlib.md5()
                        for line in file:
                            m.update(line)
                            send_size = file.tell()
                            self.client.sendall(line)
                            self.__progress(send_size, file_size, "上传中")  # 进度条
                    self.client.sendall(m.hexdigest().encode())     #发送文件md5值
                    status_code = self.client.recv(1024).decode()  #返回状态码
                    if status_code == "203":
                        print("\n文件具有一致性")
                else:print("[%s] Error！"%(status_code))
            else:
                print("[402] Error")
        else: print("[401] Error")

    def dir(self,command):
        '''查看当前目录下的文件'''
        self.__universal_method_data(command)
        pass

    def pwd(self,command):
        '''查看当前用户路径'''
        self.__universal_method_data(command)
        pass

    def mkdir(self,command):
        '''创建目录'''
        self.__universal_method_none(command)
        pass

    def cd(self,command):
        '''切换目录'''
        self.__universal_method_none(command)
        pass

    def __progress(self, trans_size, file_size,mode):
        '''
        显示进度条
        trans_size: 已经传输的数据大小
        file_size: 文件的总大小
        mode: 模式
        '''
        bar_length = 100    #进度条长度
        percent = float(trans_size) / float(file_size)
        hashes = '=' * int(percent * bar_length)    #进度条显示的数量长度百分比
        spaces = ' ' * (bar_length - len(hashes))    #定义空格的数量=总长度-显示长度
        sys.stdout.write(
            "\r%s:%.2fM/%.2fM %d%% [%s]"%(mode,trans_size/1048576,file_size/1048576,percent*100,hashes+spaces))
        sys.stdout.flush()

    def __universal_method_none(self,command):
        '''通用方法，无data输出'''
        self.client.sendall(command.encode())  # 发送要执行的命令
        status_code = self.client.recv(1024).decode()
        if status_code == "201":  # 命令可执行
            self.client.sendall("000".encode())  # 系统交互
        else:
            print("[%s] Error！" % (status_code))

    def __universal_method_data(self,command):
        '''通用方法，有data输出'''
        self.client.sendall(command.encode())   #发送要执行的命令
        status_code = self.client.recv(1024).decode()
        if status_code == "201":    #命令可执行
            self.client.sendall("000".encode())      #系统交互
            data = self.client.recv(1024).decode()
            print(data)
        else:print("[%s] Error！" % (status_code))

if __name__ == "__main__":
    ip_port =("127.0.0.1",9999)         #服务端ip、端口
    client = Myclient(ip_port)            #创建客户端实例
    client.start()                      #开始连接

